"""V-beta hygiene fixes — surgical line-by-line property-value substitutions.

Operates on .kicad_sch files in BINARY MODE. Touches only the bytes inside
property values; never modifies whitespace, line endings, indentation, or
S-expression structure.

Fixes:
  1. Footprint namespace cleanup (unique-string replacements):
     - `components:IND-SMD_L1.6-W0.8_FTC160865SR47MBCA` -> `4in1ESC:...`
     - `components:QFN-24_L4.0-W4.0-P0.50-TL-EP2.8`     -> `4in1ESC:...`
     - `ESCLibrary:QFN-28_L4.0-W4.0-P0.40-TL-EP2.4`     -> `4in1ESC:...`
  2. Cap/resistor footprint namespace swap (Reference-scoped):
     - Resistor (Reference R*) using `Capacitor_SMD:C_<size>` -> `Resistor_SMD:R_<size>`
     - Capacitor (Reference C* / CL*) using `Resistor_SMD:R_<size>` -> `Capacitor_SMD:C_<size>`

Verifies with dry-run output then writes files in-place. Run with --apply
to write; default is dry-run.
"""
import re
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
FILES = [PROJECT / "4in1ESC.kicad_sch", PROJECT / "ESC.kicad_sch"]

# Unique-string footprint substitutions (byte-level, exact match).
UNIQUE_SUBS = [
    (b'"components:IND-SMD_L1.6-W0.8_FTC160865SR47MBCA"',
     b'"4in1ESC:IND-SMD_L1.6-W0.8_FTC160865SR47MBCA"'),
    (b'"components:QFN-24_L4.0-W4.0-P0.50-TL-EP2.8"',
     b'"4in1ESC:QFN-24_L4.0-W4.0-P0.50-TL-EP2.8"'),
    (b'"ESCLibrary:QFN-28_L4.0-W4.0-P0.40-TL-EP2.4"',
     b'"4in1ESC:QFN-28_L4.0-W4.0-P0.40-TL-EP2.4"'),
]

# Reference designator pattern (within a Reference property line)
REF_RE = re.compile(rb'\(property "Reference" "([^"]+)"')
FP_RE = re.compile(rb'\(property "Footprint" "([^"]+)"')

# Library-cache fence. Inside (lib_symbols ...), property values are template
# defaults — we leave them alone. They match Reference="C", "R", "U", etc.
# Only operate on instance blocks (outside lib_symbols).


def find_lib_symbols_range(data: bytes):
    """Return (start, end) byte offsets of the (lib_symbols ...) block, or None."""
    m = re.search(rb'\(lib_symbols\b', data)
    if not m:
        return None
    start = m.start()
    # Match parens
    depth = 0
    i = start
    while i < len(data):
        c = data[i:i+1]
        if c == b'(':
            depth += 1
        elif c == b')':
            depth -= 1
            if depth == 0:
                return start, i + 1
        i += 1
    return None


def cap_resistor_swap(fp: bytes, ref: bytes) -> bytes:
    """Swap Resistor_SMD: <-> Capacitor_SMD: based on Reference designator type."""
    # Capacitor refs: C, CL (but not Conn, Crystal, etc.)
    if ref.startswith((b'C', b'CL')):
        # Plain C followed by digit, or CL followed by digit
        if re.match(rb'^(C|CL)\d', ref):
            if fp.startswith(b'Resistor_SMD:R_'):
                return b'Capacitor_SMD:C_' + fp[len(b'Resistor_SMD:R_'):]
    # Resistor refs: R followed by digit (skip Rsense which already has correct fp)
    if ref.startswith(b'R') and re.match(rb'^R\d', ref):
        if fp.startswith(b'Capacitor_SMD:C_'):
            return b'Resistor_SMD:R_' + fp[len(b'Capacitor_SMD:C_'):]
    return fp


def process(path: Path, apply: bool) -> int:
    data = path.read_bytes()
    original = data

    # ---- pass 1: unique-string namespace fixes (everywhere safe) ----
    unique_count = 0
    for old, new in UNIQUE_SUBS:
        cnt = data.count(old)
        if cnt > 0:
            data = data.replace(old, new)
            unique_count += cnt

    # ---- pass 2: cap/resistor swap, line-based, skipping lib_symbols block ----
    lib_range = find_lib_symbols_range(data)
    swap_count = 0

    # Operate line-by-line outside lib_symbols
    out_chunks = []
    cursor = 0
    if lib_range:
        # process before lib_symbols
        before = data[cursor:lib_range[0]]
        new_before, n = swap_in_chunk(before)
        out_chunks.append(new_before)
        swap_count += n
        # keep lib_symbols block verbatim
        out_chunks.append(data[lib_range[0]:lib_range[1]])
        cursor = lib_range[1]
    # process after lib_symbols (or whole file if no lib_symbols)
    rest = data[cursor:]
    new_rest, n = swap_in_chunk(rest)
    out_chunks.append(new_rest)
    swap_count += n

    new_data = b"".join(out_chunks)

    # Sanity: paren balance must match the original.
    orig_open = original.count(b'(')
    orig_close = original.count(b')')
    new_open = new_data.count(b'(')
    new_close = new_data.count(b')')
    paren_ok = (orig_open == new_open) and (orig_close == new_close)

    # Sanity: line count must match (we don't add/remove newlines).
    orig_nl = original.count(b'\n')
    new_nl = new_data.count(b'\n')
    nl_ok = orig_nl == new_nl

    diff = len(new_data) - len(original)
    print(f"\n[{path.name}]")
    print(f"  unique-string footprint subs: {unique_count}")
    print(f"  cap/resistor swap subs:       {swap_count}")
    print(f"  size delta: {diff:+d} bytes")
    print(f"  paren balance preserved:  open {orig_open}->{new_open}, close {orig_close}->{new_close}  [{ 'OK' if paren_ok else 'FAIL' }]")
    print(f"  newline count preserved:  {orig_nl}->{new_nl}  [{ 'OK' if nl_ok else 'FAIL' }]")

    if not (paren_ok and nl_ok):
        print(f"  ERROR: structural integrity broken — refusing to write.")
        return 0

    if apply and new_data != original:
        path.write_bytes(new_data)
        print(f"  -> wrote {path.name}")
    elif new_data == original:
        print(f"  (no changes)")
    else:
        print(f"  (dry-run; pass --apply to write)")
    return unique_count + swap_count


def swap_in_chunk(chunk: bytes):
    """Walk lines, tracking last-seen Reference, swap Footprint values."""
    lines = chunk.split(b'\n')
    last_ref = None
    n = 0
    for i, line in enumerate(lines):
        m = REF_RE.search(line)
        if m:
            last_ref = m.group(1)
            continue
        m = FP_RE.search(line)
        if m and last_ref is not None:
            old_fp = m.group(1)
            new_fp = cap_resistor_swap(old_fp, last_ref)
            if new_fp != old_fp:
                old_quoted = b'"' + old_fp + b'"'
                new_quoted = b'"' + new_fp + b'"'
                lines[i] = line.replace(old_quoted, new_quoted, 1)
                n += 1
            # Note: Reference-tracking persists across multiple Footprint
            # lines if any (rare; one Footprint per symbol typically).
    return b'\n'.join(lines), n


if __name__ == "__main__":
    apply = "--apply" in sys.argv
    total = 0
    for p in FILES:
        if p.exists():
            total += process(p, apply)
    print(f"\nTOTAL substitutions: {total}")
    if not apply:
        print("Dry run. Pass --apply to write changes.")
