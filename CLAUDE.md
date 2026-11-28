# CLAUDE.md: start here

Orientation for an AI assistant working on this repo. Read this first, then `knowledge/c64-verified.md`
before testing anything. `HANDOFF.md` holds the full history and every decision; search it, don't
read it all.

## What this is

*Thinking in C64 BASIC*: a book teaching Commodore 64 BASIC V2 as organized thinking, written for a
young adult beginner (a beta tester) with an editor who reviews everything. A companion **Reference**
volume. A local **course site** (C64 emulator, study view, workbook, save slots, Editor's view).
PRIVACY: the repo is public. Never name the student or his relationship to the editor, and keep
personal circumstances out of every file.

## Where things are

| Path | What |
| --- | --- |
| `book/chapters/*.md` | Book source. First line `<!-- status: final -->` or `testing`. `## Beta tester questions` sections go to the workbook only. |
| `reference/*.md`, `reference/entries/*.json`, `reference/keywords.json` | Reference source. Entries are JSON, one file per family. |
| `knowledge/` | Verified facts for future sessions (read before testing). |
| `site/` | Course site (PHP router + API, pages, `assets/c64.js`). Runs locally only. |
| `tools/` | Builds, tours, harness, verifiers. |
| `docs/` | What GitHub Pages serves (built book, tours, reference, locked editor's edition). |

## Commands

| Task | Command |
| --- | --- |
| Book, public | `python tools/build.py --student --pages` |
| Book, editor's (then lock it) | `python tools/build.py --no-pdf` then `C64BOOK_PASSWORD=... python tools/lock_editor.py` (ask the editor for the password; never commit it) |
| Reference | `python tools/build_reference.py` |
| Verify the reference | `python tools/verify_reference.py <chrome>` (needs the site running) |
| Tours | `python tools/capture_tour.py <chrome>` (needs the site), then `python tools/build_tour.py` |
| Site, in the sandbox | `php -S 127.0.0.1:8064 -t site site/router.php &` (needs `runtime/`) |

**GitHub builds it.** `.github/workflows/build.yml` runs on every push that touches `book/`, `reference/`
or `tools/`: it builds the public book (HTML + PDF, with the real web fonts, which the offline sandbox
lacks), the reference, and `site/content.json` / `site/exercises.json`, then commits them as
github-actions[bot], and Pages publishes. So push SOURCES ONLY and `git pull` before the next commit.
The locked editor's edition is built there only once the owner adds the `C64BOOK_PASSWORD` secret;
until then, build and lock it locally. Tour screenshots stay local (they need the emulator and ROMs).
The machine account's token now includes `workflow` scope (granted deliberately by the editor).

## Cost ladder: cheapest first

**Answering is not publishing (editor's rule).** In conversation, answer from knowledge, this repo's
files and reasoning, and say which it is ("I believe...", "from the reference..."). Run the emulator
ONLY (a) to verify something before it goes into the book or the reference, or (b) when the editor
asks ("validate that"). A question like "does X exist?" is a lookup, not a test run.
Other economies: screenshots only when structure checks can't answer; batch edits into one build
and one push; use --no-pdf and skip tour recaptures until a change is final; grep files instead of
printing them; keep replies short when the answer is simple.

1. **Read** `knowledge/c64-verified.md`, the reference JSON, and `HANDOFF.md` (search it). If the fact is there, no test.
2. **Read the ROM's logic**, not the whole ROM: download once to /tmp and search, e.g.
   `curl -s -o /tmp/d.txt https://raw.githubusercontent.com/mist64/c64ref/master/src/c64disasm/c64disasm_en.txt`
   then `grep -n "\*\*\* perform MID" /tmp/d.txt` and read ~60 lines. (Commented BASIC + KERNAL, ROM 901227-03.)
   Good for rules: ranges, error conditions, why something happens.
3. **One batched test** with `tools/c64_harness.py` (tokenizes BASIC and pokes it into memory; types only RUN).
   Good for exact output: spaces, digits, error text. Batch all cases of a family in one run.
4. Record every new verified fact in `knowledge/c64-verified.md` so it is never tested again.

## Pitfalls that already cost time (don't repeat them)

- **Never verify by typing through vc64web**: `wasm_auto_type` garbles shifted characters in some
  sequences, and Playwright key events drop RETURNs. Use the harness (memory poke + `run`).
- When reading the screen after typing, the **typed line** appears before `LIST`'s output: take the last match.
- Lines typed at **80 characters** are lost (the cursor wraps; RETURN enters the empty row). Keep test lines ≤ 79.
- After sign-in, wait for the exact URL (`.../c64`), not a glob: `login?next=/c64` also ends in `/c64`.
- A clip screenshot outside the viewport fails: scroll the element into view first.
- Name collisions in our own code happened three times (`$c`, `text`): one name, one meaning.
- The editor's portable PHP has no mbstring: never use `mb_*` functions (a save failed with 500). Use `preg_*` with `/u`.
- `pandoc` treats `$80...$CB` as math: the reference build disables `tex_math_dollars`.
- `docs/` paths differ per edition: book links to the reference use `%REF%` (build swaps it).

## Standing rules (details in HANDOFF.md)

Simplify, never falsify. Known limits, no loopholes. Rules, not innards (book). Reference uses exact
terminology and states what it is (no "what it's not"). Verify every example on the C64 before
publishing. Exercises use only what's been taught. Positive-value examples, varied. Chapters are born
"testing"; the editor declares them final. Each chapter is required once; coming back is welcome.
Quiz answers are checkboxes that act like radio buttons (arrow keys must not change answers).
