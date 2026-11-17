"""Build the book from book/chapters/*.md into HTML and PDF.

Usage:
    python tools/build.py              editor's edition (answers shown)
    python tools/build.py --student    student's edition (answers removed)
    python tools/build.py --student --pages   student's edition into docs/ for GitHub Pages

Output goes to build/. Needs: pip install pypandoc_binary weasyprint
"""
import argparse, datetime, pathlib, re
import pypandoc

ROOT = pathlib.Path(__file__).resolve().parent.parent
TITLE = "Thinking in C64 BASIC"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--student", action="store_true", help="remove quiz answers")
    ap.add_argument("--no-pdf", action="store_true", help="skip the PDF")
    ap.add_argument("--pages", action="store_true", help="write to docs/ for GitHub Pages")
    args = ap.parse_args()

    chapters = sorted((ROOT / "book" / "chapters").glob("*.md"))
    text = "\n\n".join(p.read_text(encoding="utf-8") for p in chapters)
    if args.student:
        text = re.sub(r"\s*\*\*Answer: [a-d]\*\*", "", text)

    edition = "Student’s edition" if args.student else "Editor’s preview"
    suffix = "student" if args.student else "editor"
    out = ROOT / ("docs" if args.pages else "build")
    out.mkdir(exist_ok=True)

    html = pypandoc.convert_text(
        text, "html5", format="markdown",
        extra_args=[
            "--standalone", "--toc", "--toc-depth=2",
            f"--template={ROOT / 'tools' / 'template.html'}",
            f"--metadata=title:{TITLE}",
            f"--metadata=edition:{edition}",
            f"--metadata=date:{datetime.date.today():%b %d, %Y}",
        ],
    )
    html_path = out / ("index.html" if args.pages else f"book-{suffix}.html")
    html_path.write_text(html, encoding="utf-8")
    print("wrote", html_path)

    if not args.no_pdf:
        from weasyprint import HTML
        pdf_path = out / ("thinking-in-c64-basic.pdf" if args.pages else f"book-{suffix}.pdf")
        HTML(string=html, base_url=str(ROOT)).write_pdf(pdf_path)
        print("wrote", pdf_path)

if __name__ == "__main__":
    main()
