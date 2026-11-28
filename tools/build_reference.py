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

def main():
    # Markdown chapters and JSON families, together in file-name order (10-keywords, 20-strings, ...).
    parts = sorted(list((ROOT / "reference").glob("*.md")) + list((ROOT / "reference" / "entries").glob("*.json")), key=lambda p: p.name)
    text = "\n\n".join(render_family(json.loads(p.read_text(encoding="utf-8"))) if p.suffix == ".json" else p.read_text(encoding="utf-8")
                       for p in parts).replace("<!--KEYWORD-INDEX-->", keyword_index())
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
