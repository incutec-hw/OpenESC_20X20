"""V-beta hygiene fixes — scoped property-value substitutions only.

Touches Footprint and lib_id property strings inside (symbol ...) blocks
in .kicad_sch files. Does not modify pin positions, geometry, hierarchy,
or any S-expression structure.

Fixes:
  1. Footprint namespace cleanup:
     - `components:<fp>` -> `4in1ESC:<fp>`  (footprint lib is "4in1ESC", not "components")
     - `ESCLibrary:<fp>` -> `4in1ESC:<fp>`  (stale lib reference)
  2. Symbol lib_id cleanup:
     - `ESCLibrary:AT32F421G8U7` -> `components:AT32F421G8U7`
  3. Cap/resistor footprint namespace swap (cosmetic but ugly on BOM):
     - Resistors (R*) using `Capacitor_SMD:C_<size>` -> `Resistor_SMD:R_<size>`
     - Caps (C*, CL*) using `Resistor_SMD:R_<size>` -> `Capacitor_SMD:C_<size>`

Verify with `git diff` before committing. The script preserves byte
order and indentation outside the substituted strings.
"""
import re
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
FILES = [PROJECT / "4in1ESC.kicad_sch", PROJECT / "ESC.kicad_sch"]

# Iterate top-level (symbol "...") blocks and operate inside each.
# Block boundary detection: count parens.

def find_symbol_blocks(text):
    """Yield (start, end, body) for each top-level (symbol ...) instance block.

    Top-level instance blocks are indented one level (one tab/4-space) and
    contain (lib_id "..."). We skip the lib_symbols cache (those are nested
    deeper or also at top level but we filter by presence of (lib_id which
    only instances have).
    """
    i = 0
    while True:
        m = re.search(r'^(\t|    )\(symbol "', text[i:], re.MULTILINE)
        if not m:
            return
        start = i + m.start()
        # find matching close paren
        depth = 0
        j = start
        while j < len(text):
            c = text[j]
            if c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
                if depth == 0:
                    j += 1
                    break
            j += 1
        body = text[start:j]
        # Filter to instance blocks (contain lib_id property)
        if re.search(r'\(lib_id "', body):
            yield start, j, body
        i = j


SIZE_TOKEN_RE = re.compile(r'_([0-9]{4})_([0-9]+)Metric')


def fix_block(body):
    """Apply substitutions within a single instance block. Return new body."""
    new = body

    ref_m = re.search(r'\(property "Reference" "([^"]+)"', new)
    fp_m = re.search(r'\(property "Footprint" "([^"]*)"', new)
    if not ref_m:
        return new
    ref = ref_m.group(1)

    if fp_m:
        old_fp = fp_m.group(1)
        new_fp = old_fp

        # Namespace cleanup
        if new_fp.startswith("components:"):
            new_fp = "4in1ESC:" + new_fp[len("components:"):]
        elif new_fp.startswith("ESCLibrary:"):
            new_fp = "4in1ESC:" + new_fp[len("ESCLibrary:"):]

        # Cap/resistor namespace swap based on Reference designator
        if ref.startswith(("CL", "C")) and not ref.startswith(("Conn", "Crystal")):
            # Capacitor: should use Capacitor_SMD:C_*
            if new_fp.startswith("Resistor_SMD:R_"):
                # Resistor_SMD:R_1206_3216Metric -> Capacitor_SMD:C_1206_3216Metric
                rest = new_fp[len("Resistor_SMD:R_"):]
                new_fp = "Capacitor_SMD:C_" + rest
        elif ref.startswith("R") and ref not in ("Reference",) and not ref.startswith("Rsense"):
            # Resistor: should use Resistor_SMD:R_*
            if new_fp.startswith("Capacitor_SMD:C_"):
                rest = new_fp[len("Capacitor_SMD:C_"):]
                new_fp = "Resistor_SMD:R_" + rest
        # Special: Rsense (current sense shunt) keeps Resistor_SMD: prefix - already correct

        if new_fp != old_fp:
            new = new.replace(
                f'(property "Footprint" "{old_fp}"',
                f'(property "Footprint" "{new_fp}"',
                1,
            )

    # lib_id cleanup (instance side): ESCLibrary:AT32F421G8U7 -> components:AT32F421G8U7
    new = re.sub(
        r'\(lib_id "ESCLibrary:([^"]+)"',
        r'(lib_id "components:\1"',
        new,
    )

    return new


def fix_lib_symbols_block(text):
    """Also rename embedded lib_symbols cache references.

    `(symbol "ESCLibrary:AT32F421G8U7"` -> `(symbol "components:AT32F421G8U7"`
    inside the lib_symbols cache section. KiCad refreshes this on save so
    the existing form would also work, but consistency is cleaner.
    """
    return re.sub(
        r'\(symbol "ESCLibrary:([A-Za-z0-9_-]+)"',
        r'(symbol "components:\1"',
        text,
    )


def process(path: Path):
    text = path.read_text(encoding="utf-8")
    new = text
    # Iterate blocks and reassemble
    out = []
    cursor = 0
    fixes = 0
    for start, end, body in find_symbol_blocks(new):
        out.append(new[cursor:start])
        fixed = fix_block(body)
        if fixed != body:
            fixes += 1
        out.append(fixed)
        cursor = end
    out.append(new[cursor:])
    rebuilt = "".join(out)
    rebuilt = fix_lib_symbols_block(rebuilt)
    if rebuilt != text:
        path.write_text(rebuilt, encoding="utf-8")
        print(f"{path.name}: rewrote ({fixes} instance blocks edited + lib_symbols cache rename)")
    else:
        print(f"{path.name}: no changes")


if __name__ == "__main__":
    for p in FILES:
        if p.exists():
            process(p)
        else:
            print(f"missing: {p}")
