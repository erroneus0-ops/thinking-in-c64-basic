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
    rows = ["| Hex | Dec | Keyword | Kind | Abbreviation | Taught in |", "| --- | --- | --- | --- | --- | --- |"]
    for d in data["keywords"]:
        rows.append(f"| ${d['token']:02X} | {d['token']} | `{d['keyword']}` | {d['kind']} | {abbr(d['abbreviation'])} | "
                    f"{('Ch. ' + d['chapter']) if d['chapter'] else '—'} |")
    p = data["pi"]
    rows.append(f"| ${p['token']:02X} | {p['token']} | π | {p['kind']} | SHIFT + ↑ | — |")
    return "All 76 keywords of BASIC V2 in token order, plus π. \"Taught in\" refers to *Thinking in C64 BASIC*.\n\n" + "\n".join(rows)

def main():
    parts = sorted((ROOT / "reference").glob("*.md"))
    text = "\n\n".join(p.read_text(encoding="utf-8") for p in parts).replace("<!--KEYWORD-INDEX-->", keyword_index())
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
