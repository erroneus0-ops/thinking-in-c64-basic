"""Verify every example and edge case in reference/entries/*.json on the course site's C64.
Examples: the code runs as a program (lines 10, 20, ...) and the screen must show exactly the listed
output. Cases: PRINT "<";expr;">" after the family's setup lines, and the result must match:
a "quoted" string, a number, or an error message (?... ERROR IN 20).
Usage: python tools/verify_reference.py [path-to-chrome]   (course site must be running)"""
import asyncio, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from c64_harness import C64

ROOT = pathlib.Path(__file__).resolve().parent.parent

def expected_row(result):
    if result.startswith('"'):
        return "<" + result[1:-1] + ">"
    return "<" + ("" if result.startswith("-") else " ") + result + " >"

async def main():
    c = await C64().open(chrome=sys.argv[1] if len(sys.argv) > 1 else None)
    failures, checks = [], 0
    for path in sorted((ROOT / "reference" / "entries").glob("*.json")):
        fam = json.loads(path.read_text(encoding="utf-8"))
        setup = [(10 + 10 * i, s) for i, s in enumerate(fam.get("setup", []))]
        for e in fam["entries"]:
            ex = e["example"]; checks += 1
            rows = await c.run([(10 * (i + 1), line) for i, line in enumerate(ex["code"])])
            if rows != ex["output"]:
                failures.append((e["keyword"], "example", ex["output"], rows))
            for expr, result, _note in e["cases"]:
                checks += 1
                n = 10 * (len(setup) + 1)
                rows = await c.run(setup + [(n, f'PRINT "<";{expr};">"')], wait=1200)
                if result.startswith("?"):
                    ok = f"{result} IN {n}" in rows
                else:
                    ok = expected_row(result) in rows
                if not ok:
                    failures.append((e["keyword"], expr, result, rows))
    await c.close()
    print(f"{checks - len(failures)} of {checks} checks passed")
    for f in failures:
        print("FAIL", f)
    sys.exit(1 if failures else 0)

if __name__ == "__main__":
    asyncio.run(main())
