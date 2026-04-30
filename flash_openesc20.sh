#!/usr/bin/env bash
# flash_openesc20.sh — Production flash script for OpenESC_20 (AT32F421G8U7)
# Flashes bootloader + AM32 firmware via ST-LINK V2 pogo-pin jig
set -euo pipefail

# ─── Paths ───────────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
UNLOCKER_DIR="/Users/stan/Library/Mobile Documents/com~apple~CloudDocs/adjustableBuck/AM32-unlocker"

OPENOCD="${UNLOCKER_DIR}/tools/macos/openocd/bin/openocd"
OPENOCD_SCRIPTS="${UNLOCKER_DIR}/tools/macos/openocd/share/openocd/scripts"
PROBE_CFG="${UNLOCKER_DIR}/probes/stlink.cfg"

BOOTLOADER="${UNLOCKER_DIR}/bootloaders/AM32_F421_BOOTLOADER_PB4_V17.bin"
FIRMWARE="/Users/stan/Documents/GitHub/AM32/obj/AM32_OPENESC_20_F421_2.20.bin"

# ─── Audio feedback (macOS) ──────────────────────────────────────────────────
sound_pass() {
    say -v Samantha "pass" &
    afplay /System/Library/Sounds/Glass.aiff &
}

sound_fail() {
    say -v Samantha "fail" &
    afplay /System/Library/Sounds/Sosumi.aiff &
}

# ─── Preflight checks ───────────────────────────────────────────────────────
for f in "$OPENOCD" "$PROBE_CFG" "$BOOTLOADER" "$FIRMWARE"; do
    if [[ ! -f "$f" ]]; then
        echo "ERROR: missing file: $f"
        exit 1
    fi
done

echo "=== OpenESC_20 Production Flash ==="
echo "Bootloader: $(basename "$BOOTLOADER")"
echo "Firmware:   $(basename "$FIRMWARE")"
echo ""

# ─── OpenOCD TCL flash script ────────────────────────────────────────────────
# Inline TCL: unlock → erase → program bootloader → verify → program firmware → verify
TCL_SCRIPT=$(cat <<'TCLEOF'
proc at32f421_disable_write_protection {} {
    set AT32_FLASH_BANK1_REG_1 0x40022000
    set AT32_USD_ADDR_1 0x1FFFF800
    set KEY1 0x45670123
    set KEY2 0xCDEF89AB

    reset halt
    wait_halt

    # Unlock flash and USD
    at32f421xx.cpu write_memory [expr $AT32_FLASH_BANK1_REG_1+0x04] 32 $KEY1
    at32f421xx.cpu write_memory [expr $AT32_FLASH_BANK1_REG_1+0x04] 32 $KEY2
    at32f421xx.cpu write_memory [expr $AT32_FLASH_BANK1_REG_1+0x08] 32 $KEY1
    at32f421xx.cpu write_memory [expr $AT32_FLASH_BANK1_REG_1+0x08] 32 $KEY2

    # Erase USD
    at32f421xx.cpu write_memory [expr $AT32_FLASH_BANK1_REG_1+0x10] 32 0x220
    at32f421xx.cpu write_memory [expr $AT32_FLASH_BANK1_REG_1+0x10] 32 0x260
    sleep 1000

    # Re-unlock after erase
    at32f421xx.cpu write_memory [expr $AT32_FLASH_BANK1_REG_1+0x04] 32 $KEY1
    at32f421xx.cpu write_memory [expr $AT32_FLASH_BANK1_REG_1+0x04] 32 $KEY2
    at32f421xx.cpu write_memory [expr $AT32_FLASH_BANK1_REG_1+0x08] 32 $KEY1
    at32f421xx.cpu write_memory [expr $AT32_FLASH_BANK1_REG_1+0x08] 32 $KEY2

    # Program USD: FAP=0xA5 (unlocked), all EPP=0xFF (no protection)
    at32f421xx.cpu write_memory [expr $AT32_FLASH_BANK1_REG_1+0x10] 32 0x210
    at32f421xx.cpu write_memory [expr $AT32_USD_ADDR_1]    16 0xA5
    at32f421xx.cpu write_memory [expr $AT32_USD_ADDR_1+2]  16 0xFF
    at32f421xx.cpu write_memory [expr $AT32_USD_ADDR_1+4]  16 0xFF
    at32f421xx.cpu write_memory [expr $AT32_USD_ADDR_1+6]  16 0xFF
    at32f421xx.cpu write_memory [expr $AT32_USD_ADDR_1+8]  16 0xFF
    at32f421xx.cpu write_memory [expr $AT32_USD_ADDR_1+10] 16 0xFF
    at32f421xx.cpu write_memory [expr $AT32_USD_ADDR_1+12] 16 0xFF
    at32f421xx.cpu write_memory [expr $AT32_USD_ADDR_1+14] 16 0xFF
    at32f421xx.cpu write_memory [expr $AT32_FLASH_BANK1_REG_1+0x10] 32 0x80
    sleep 1000

    reset halt
}

init
reset halt

echo ">>> Unlocking flash protection..."
at32f421_disable_write_protection

echo ">>> Erasing sectors 0-4..."
init
reset halt
flash erase_sector 0 0 4

echo ">>> Programming bootloader..."
flash write_bank 0 __BOOTLOADER__

echo ">>> Verifying bootloader..."
flash verify_bank 0 __BOOTLOADER__

echo ">>> Programming firmware at offset 0x1000..."
flash write_bank 0 __FIRMWARE__ 0x1000

echo ">>> Verifying firmware..."
flash verify_bank 0 __FIRMWARE__ 0x1000

echo ">>> ALL DONE"
exit
TCLEOF
)

# Substitute actual file paths into TCL script
TCL_SCRIPT="${TCL_SCRIPT//__BOOTLOADER__/$BOOTLOADER}"
TCL_SCRIPT="${TCL_SCRIPT//__FIRMWARE__/$FIRMWARE}"

# ─── Flash one board ─────────────────────────────────────────────────────────
flash_one() {
    local tmpfile
    tmpfile=$(mktemp /tmp/flash_openesc20.XXXXXX.cfg)
    # Compose full OpenOCD config: probe + target + TCL script
    {
        cat "$PROBE_CFG"
        echo 'source [find target/at32f421xx.cfg]'
        echo "$TCL_SCRIPT"
    } > "$tmpfile"

    echo "--- Flashing board ---"
    local start_time
    start_time=$(date +%s)

    if "$OPENOCD" -s "$OPENOCD_SCRIPTS" -f "$tmpfile" 2>&1; then
        local elapsed=$(( $(date +%s) - start_time ))
        echo ""
        echo "=== PASS (${elapsed}s) ==="
        sound_pass
        rm -f "$tmpfile"
        return 0
    else
        local elapsed=$(( $(date +%s) - start_time ))
        echo ""
        echo "=== FAIL (${elapsed}s) ==="
        sound_fail
        rm -f "$tmpfile"
        return 1
    fi
}

# ─── Wait for ST-LINK disconnect/reconnect ───────────────────────────────────
wait_for_stlink_disconnect() {
    echo "Waiting for board removal (ST-LINK disconnect)..."
    while system_profiler SPUSBDataType 2>/dev/null | grep -qi "ST-LINK"; do
        sleep 0.3
    done
    echo "Board removed."
}

wait_for_stlink_connect() {
    echo "Waiting for next board (ST-LINK connect)..."
    while ! system_profiler SPUSBDataType 2>/dev/null | grep -qi "ST-LINK"; do
        sleep 0.3
    done
    # Brief settle time for USB enumeration
    sleep 0.5
    echo "ST-LINK detected."
}

# ─── Main ────────────────────────────────────────────────────────────────────
LOOP_MODE=false
if [[ "${1:-}" == "--loop" ]]; then
    LOOP_MODE=true
    echo "Loop mode enabled — swap boards on jig, auto-flashes next."
    echo ""
fi

PASS_COUNT=0
FAIL_COUNT=0

while true; do
    flash_one && PASS_COUNT=$((PASS_COUNT + 1)) || FAIL_COUNT=$((FAIL_COUNT + 1))

    if [[ "$LOOP_MODE" == false ]]; then
        break
    fi

    echo ""
    echo "Score: ${PASS_COUNT} pass / ${FAIL_COUNT} fail"
    echo ""
    wait_for_stlink_disconnect
    wait_for_stlink_connect
done

if [[ "$LOOP_MODE" == true ]]; then
    echo ""
    echo "Final score: ${PASS_COUNT} pass / ${FAIL_COUNT} fail"
fi
