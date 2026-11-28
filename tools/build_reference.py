"""Build the reference volume: docs/reference/index.html and docs/reference/thinking-in-c64-basic-reference.pdf.
Source: reference/*.md in name order; the keyword index table is generated from reference/keywords.json."""
import datetime, json, pathlib, sys
import pypandoc
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build import ROOT, mark_return_keys

def keyword_index():
    data = json.loads((ROOT / "reference" / "keywords.json").read_text(encoding="utf-8"))
    def abbr(a):
        return f"{a[:-1].upper()} ⇧{a[-1]}" if a else "—"
    with_entry = entry_keywords()
    rows = ["| Hex | Dec | Keyword | Kind | Abbreviation | Taught in |", "| --- | --- | --- | --- | --- | --- |"]
    for d in data["keywords"]:
        kw = f"[`{d['keyword']}`](#{anchor(d['keyword'])})" if d["keyword"] in with_entry else f"`{d['keyword']}`"
        rows.append(f"| ${d['token']:02X} | {d['token']} | {kw} | {d['kind']} | {abbr(d['abbreviation'])} | "
                    f"{('Ch. ' + d['chapter']) if d['chapter'] else '—'} |")
    p = data["pi"]
    rows.append(f"| ${p['token']:02X} | {p['token']} | π | {p['kind']} | SHIFT + ↑ | — |")
    return "All 76 keywords of BASIC V2 in token order, plus π. \"Taught in\" refers to *Thinking in C64 BASIC*.\n\n" + "\n".join(rows)

def anchor(keyword):
    """A stable link anchor for a keyword's entry: MID$ -> kw-mids, PRINT# -> kw-printhash."""
    return "kw-" + keyword.lower().replace("$", "s").replace("#", "hash").replace("(", "")

def keyword_info():
    data = json.loads((ROOT / "reference" / "keywords.json").read_text(encoding="utf-8"))
    return {d["keyword"]: d for d in data["keywords"]}

def entry_keywords():
    found = set()
    for p in (ROOT / "reference" / "entries").glob("*.json"):
        for e in json.loads(p.read_text(encoding="utf-8"))["entries"]:
            found.add(e["keyword"])
    return found

def code(s):
    return "`" + s + "`"

def render_family(fam):
    """One family of entries, from JSON to Markdown, every entry in the same shape."""
    info = keyword_info()
    md = [f"# {fam['family']}", "", fam.get("intro", ""), ""]
    for e in fam["entries"]:
        k, d = e["keyword"], info[e["keyword"]]
        ab = f"{d['abbreviation'][:-1].upper()} ⇧{d['abbreviation'][-1]}" if d["abbreviation"] else "none"
        md += [f"## {k} {{#{anchor(k)}}}", "",
               f"**Token** ${d['token']:02X} ({d['token']}) · **Kind** {d['kind']} · **Abbreviation** {ab} · "
               f"**Taught in** {('Chapter ' + d['chapter']) if d['chapter'] else '—'}", "",
               "```{.syntax}", e["syntax"], "```", "",
               f"**Returns** a {e['returns']}.", "",
               "| Argument | Type | Meaning |", "| --- | --- | --- |"]
        md += [f"| *{a}* | {t} | {m} |" for a, t, m in e["arguments"]]
        md += ["", e["description"], "", "**Example**", ""]
        width = max(len(v) for v, _ in e["example"]["vars"])
        md += ["```{.vars}"] + [f"{v.ljust(width)} : {role}" for v, role in e["example"]["vars"]] + ["```", ""]
        md += ["```"] + e["example"]["code"] + ["```", ""]
        md += ["```{.output}"] + e["example"]["output"] + ["```", ""]
        md += ["**Edge cases**", "", "| Expression | Result | Note |", "| --- | --- | --- |"]
        md += [f"| {code(x)} | {code(r) if not r.startswith('?') else r} | {n} |" for x, r, n in e["cases"]]
        md += [""]
        if e["errors"]:
            md += ["**Errors** " + " ".join(e["errors"]), ""]
        md += ["**Related** " + ", ".join(f"[{code(r)}](#{anchor(r)})" for r in e["related"]), ""]
    return "\n".join(md)

COLOR_NAMES = {144: (0, "black"), 5: (1, "white"), 28: (2, "red"), 159: (3, "cyan"), 156: (4, "purple"), 30: (5, "green"),
  31: (6, "blue"), 158: (7, "yellow"), 129: (8, "orange"), 149: (9, "brown"), 150: (10, "light red"), 151: (11, "dark grey"),
  152: (12, "grey"), 153: (13, "light green"), 154: (14, "light blue"), 155: (15, "light grey")}

def render_petscii(d):
    """The PETSCII chart: readable tables, with explanations as numbered notes after them."""
    sup = "¹²³⁴⁵⁶⁷⁸⁹"
    def typed(r):
        return " or ".join(r["type"]) if r["type"] else "—"
    md = ["# PETSCII and screen codes", "",
          "The C64 uses two numbering systems for characters. **PETSCII** codes are what `CHR$` returns, what "
          "`ASC` reads and what `PRINT` sends. **Screen codes** are what screen memory holds, so they are what "
          "`POKE` writes to and `PEEK` reads from the screen (address 1024 onward). The letter A is PETSCII 65 "
          "but screen code 1.", "",
          "## Control codes", "",
          "Printing a control code performs an action instead of showing a character. Codes not listed here "
          "(within 0–31 and 128–159) do nothing when printed.", "",
          "| Dec | Hex | Code | Type it | Note |", "| --- | --- | --- | --- | --- |"]
    for r in d["rows"]:
        if r["control"]:
            n = sup[r["note"] - 1] if r["note"] else ""
            md.append(f"| {r['code']} | ${r['code']:02X} | {r['char']} | {typed(r)} | {n} |")
    md += ["", "## Printable characters", "",
           "Graphics characters are identified by the key combination that types them, which matches the "
           "symbols printed on the front of the C64's keys (SHIFT: right symbol; C=: left symbol). Several "
           "codes show the same character; \"Same as\" gives the first code with the same screen code.", "",
           "| Dec | Hex | Character | Type it | Screen code | Same as |", "| --- | --- | --- | --- | --- | --- |"]
    first = {}
    for r in d["rows"]:
        if r["control"]:
            continue
        same = first.setdefault(r["screen"], r["code"])
        ch = f"`{r['char']}`" if r["char"] and r["char"] != " " else ("space" if r["char"] == " " else "*graphic*")
        md.append(f"| {r['code']} | ${r['code']:02X} | {ch} | {typed(r)} | {r['screen']} | {same if same != r['code'] else ''} |")
    md += ["", "## Notes", ""]
    colors = ", ".join(f"{code} {name} ({num})" for code, (num, name) in sorted(COLOR_NAMES.items(), key=lambda x: x[1][0]))
    md += [f"1. **Color codes** set the color of characters printed afterwards. Code, color, and the color number used "
           f"by `POKE` to color memory (55296 onward) and to the border and background registers: {colors}.",
           "2. **REVERSE ON** prints the following characters in reverse (screen code plus 128) until **REVERSE OFF**.",
           "3. **LOWER CASE** switches the whole screen at once to the lower-case/upper-case character set "
           "(register 53272 changes from 21 to 23); **UPPER CASE** switches back to upper-case/graphics. In the "
           "lower-case set, codes 65–90 display as lower-case letters and 193–218 as capitals. SHIFT + C= switches "
           "the same way from the keyboard.",
           "4. **LOCK CASE** prevents SHIFT + C= from switching character sets (location 657 becomes 128); "
           "**UNLOCK CASE** allows it again (657 becomes 0).",
           "5. **Cursor movement**: printing these moves the cursor exactly as the keys do. **HOME** moves it to the "
           "top left corner; **CLEAR** also erases the screen.",
           "6. **DELETE** removes the character to the left of the cursor and closes the gap; **INSERT** opens a gap "
           "at the cursor.",
           "7. **RETURN** moves the cursor to the start of the next line. Typed, SHIFT + RETURN moves to the next "
           "line without entering the current one.",
           "8. **Function keys** produce these codes when pressed, for programs to read with `GET`.",
           "",
           "Inside quotation marks, typed control codes are stored in the string instead of being performed, "
           "and are shown as reversed characters (quote mode).", "",
           f"*{d['verified']}*"]
    return "\n".join(md)

def main():
    # Markdown chapters and JSON families, together in file-name order (10-keywords, 20-strings, ...).
    parts = sorted(list((ROOT / "reference").glob("*.md")) + list((ROOT / "reference").glob("[0-9]*.json"))
                   + list((ROOT / "reference" / "entries").glob("*.json")), key=lambda p: p.name)
    def render(p):
        if p.suffix != ".json":
            return p.read_text(encoding="utf-8")
        d = json.loads(p.read_text(encoding="utf-8"))
        return render_petscii(d) if d.get("kind") == "petscii" else render_family(d)
    text = "\n\n".join(render(p) for p in parts).replace("<!--KEYWORD-INDEX-->", keyword_index())
    out = ROOT / "docs" / "reference"
    out.mkdir(parents=True, exist_ok=True)
    html = pypandoc.convert_text(text, "html5", format="markdown-tex_math_dollars", extra_args=[   # $80 is a token number, not math
        "--standalone", "--toc", "--toc-depth=2",
        f"--template={ROOT / 'tools' / 'template.html'}",
        "--metadata=title:Thinking in C64 BASIC: Reference",
        "--metadata=edition:Reference volume",
        f"--metadata=date:{datetime.date.today():%b %d, %Y}",
    ])
    html = mark_return_keys(html)
    (out / "index.html").write_text(html, encoding="utf-8")
    print("wrote", out / "index.html")
    if "--no-pdf" not in sys.argv:
        from weasyprint import HTML
        HTML(string=html, base_url=str(ROOT)).write_pdf(out / "thinking-in-c64-basic-reference.pdf")
        print("wrote", out / "thinking-in-c64-basic-reference.pdf")

if __name__ == "__main__":
    main()
