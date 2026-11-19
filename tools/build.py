"""Build the book from book/chapters/*.md into HTML and PDF.

Usage:
    python tools/build.py              editor's edition (answers shown)
    python tools/build.py --student    student's edition (answers removed)
    python tools/build.py --student --pages   student's edition into docs/ for GitHub Pages

Output goes to build/. Needs: pip install pypandoc_binary weasyprint
"""
import argparse, datetime, json, pathlib, re
import pypandoc

ROOT = pathlib.Path(__file__).resolve().parent.parent
TITLE = "Thinking in C64 BASIC"

def plain(md):
    """Markdown inline text to plain text for the course site."""
    md = re.sub(r"\*\*(.+?)\*\*", r"\1", md)
    md = re.sub(r"`([^`]*)`", r"\1", md)
    return md.strip()

def extract_content(chapters):
    """Pull lessons, exercises and quizzes out of the chapter files for the course site.
    Writes site/content.json (the server grades quizzes from it; answers never go to the page)."""
    out = []
    for path in chapters:
        if path.stem.startswith("9"):   # appendices: reference pages, no lessons or quizzes
            continue
        text = path.read_text(encoding="utf-8")
        m = re.search(r"^# Chapter (\d+): (.+)$", text, re.M)
        if m:
            n, title = int(m.group(1)), m.group(2).strip()
            lessons = [{"id": a, "title": b.strip()} for a, b in re.findall(r"^## Lesson (\d+\.\d+) — (.+)$", text, re.M)]
        else:  # opening pages: one "lesson" per file, as chapter 0
            n, title = 0, "Before you begin"
            h = re.search(r"^# (.+)$", text, re.M)
            lessons = [{"id": path.stem, "title": h.group(1).strip()}] if h else []
        ch = next((c for c in out if c["n"] == n), None)
        if not ch:
            ch = {"n": n, "title": title, "lessons": [], "exercises": [], "quiz": []}
            out.append(ch)
        ch["lessons"] += lessons
        ex = re.search(r"^## Exercises\n(.*?)(?=^## |\Z)", text, re.M | re.S)
        if ex:
            for num, body in re.findall(r"^(\d+)\. (.+?)(?=^\d+\. |\Z)", ex.group(1), re.M | re.S):
                t = re.match(r"\*\*(.+?)\*\*\s*(.*)", body.strip(), re.S)
                ch["exercises"].append({"n": int(num), "title": plain(t.group(1)).rstrip(".") if t else "",
                                        "text": plain(t.group(2) if t else body)})
        qz = re.search(r"^## Quiz\n(.*?)(?=^## |\Z)", text, re.M | re.S)
        if qz:
            for num, body in re.findall(r"^(\d+)\. (.+?)(?=^\d+\. |\Z)", qz.group(1), re.M | re.S):
                ans = re.search(r"\*\*Answer: ([a-d])\*\*", body)
                body = re.sub(r"\s*\*\*Answer: [a-d]\*\*", "", body).strip()
                parts = re.split(r"\s*\(([a-d])\)\s*", body)
                question, opts = parts[0], parts[1:]
                options = [{"letter": opts[i], "text": plain(opts[i + 1]).rstrip(".")} for i in range(0, len(opts), 2)]
                ch["quiz"].append({"n": int(num), "question": plain(question), "options": options,
                                   "answer": ans.group(1) if ans else None})
    (ROOT / "site" / "content.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print("wrote", ROOT / "site" / "content.json")
    # The C64 page's exercise picker: free practice, then every exercise from Chapter 2 on
    # (Chapter 1 works in direct mode, so it has no programs to submit).
    picker = [{"id": "practice", "title": "Free practice"}] + [
        {"id": f"ch{c['n']:02d}-ex{e['n']}", "title": f"Chapter {c['n']}, exercise {e['n']}: {e['title']}"}
        for c in out if c["n"] >= 2 for e in c["exercises"]]
    (ROOT / "site" / "exercises.json").write_text(json.dumps(picker, indent=1, ensure_ascii=False), encoding="utf-8")

def mark_return_keys(html):
    """Every line in a typed code block gets a RETURN keycap at its end (drawn by CSS, so it is
    never part of the text). Diagram blocks are left alone."""
    def mark(m):
        lines = m.group(1).split("\n")
        return "<pre><code>" + "\n".join(f'<span class="ln">{l}</span>' if l.strip() else l for l in lines) + "</code></pre>"
    return re.sub(r"<pre><code>(.*?)</code></pre>", mark, html, flags=re.S)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--student", action="store_true", help="remove quiz answers")
    ap.add_argument("--no-pdf", action="store_true", help="skip the PDF")
    ap.add_argument("--pages", action="store_true", help="write to docs/ for GitHub Pages")
    args = ap.parse_args()

    chapters = sorted((ROOT / "book" / "chapters").glob("*.md"))
    extract_content(chapters)
    text = "\n\n".join(p.read_text(encoding="utf-8") for p in chapters)
    if args.student:
        text = re.sub(r"\s*\*\*Answer: [a-d]\*\*", "", text)

    edition = "Beta tester’s draft" if args.student else "Editor’s draft, with answers"
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
            # The tour link appears only in the published HTML (the student page at the site's root,
            # and the editor's page, which is locked into docs/editor/).
            f"--metadata=tourhref:{'tour/' if args.pages else '../tour/'}",
        ],
    )
    html = mark_return_keys(html)
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
