# Handoff notes

Read this first in every new session. Update it at the end of each session.

## Privacy rule

This repo is PUBLIC. Describing the target audience is fine. Never name the student
or say how he is related to anyone on the project.

## Target audience

A young adult beginner with no programming experience. Bright and strong in spatial
reasoning; good at video games; easily distracted, so lessons are short and every
lesson ends with something that runs. Basic math and logic are reasonable but benefit
from extra practice and repetition. Interested in writing fiction (hence the Story
Engine project). The goal is less "learn C64 BASIC" than "use programming to build
organized, orderly thinking habits."

## People and roles

- **Repo owner** (`erroneus0-ops`): editor. Decides platform and content questions.
- **Claude**: C64 subject expert and author. Works through the machine account
  `C64BookDev`, scoped to this one private repo
  (see the owner's `MACHINE_ACCOUNT_SETUP_GUIDE.md` in `erroneus0-ops/WebUI-debug-dev`).

## Where things are

- Book plan, editing copy: the Claude Doc "Thinking in C64 BASIC — Book Plan &
  Chapter 1 Draft" (https://claude.ai/artifact/PJj9Ywwp1HJwWLtHqncpUm). The editor edits and
  comments there while the plan is in flux.
- `book/plan.md`: snapshot of that doc (re-export after changes; drop the byline line).
  The Claude Doc is the source of truth for the plan.
- `book/chapters/NN-name.md`: the book itself, one file per chapter. These are the source
  of truth for chapter text (Chapter 1 now lives here, not in the plan).
- Public site (student edition, no answers): GitHub Pages from the `docs/` folder.
- Private preview of the editor's edition (with answers), republished after each change:
  https://claude.ai/artifact/8oDEifbK2sqmeAtf1hiy9t

## Building the book

`pip install -r tools/requirements.txt`, then `python tools/build.py` (editor's edition,
answers shown, output in `build/`) or `python tools/build.py --student --pages` (answers
removed, written to `docs/` for the public site). Commit `docs/` after building. Pandoc Markdown; template and styles in `tools/template.html`.

Content ideas from the editor (to place in chapters):
- Chapter 7 price checker: "buy only at the maker's price, never collector prices"; markup percent.
- Wish list with a waiting period; Spending Tracker flags purchases above the maker's price.
- Variable dictionary gets units in "What it holds" (e.g. "in cents"); Mars Climate Orbiter story.
- Arrays: the Roman calendar off-by-two (September = 7th month, now 9th).
- Sorting (Ch 14): box 0 is the "parking space" for swaps (A(0)=A(I):A(I)=A(I+1):A(I+1)=A(0)).
  This is box 0's first "special job", promised in Ch 13.
- TI jiffies (1/60 s) to HH:MM:SS with INT and division.
- Sprites: a Windows-style spinner ("baller coaster") with 8 sprites and a DATA position table.
- Premise gains the habit "know the subject before you write the code."

Conventions in chapter files:
- Plain fenced code block = something to type. Renders as a C64 screen.
- ` ```{.diagram} ` fenced block = a picture, not to be typed. Renders as a dashed box.
- Quiz answers written as `**Answer: x**` at the end of each question; the student build
  strips them.

## Course site (Milestones 1-3 drafted)

- Design doc (private Claude Doc): "Work Environment - Implementation Sketch",
  https://claude.ai/artifact/8Ze8EH2K5wBTC686yjHn4T
- `setup.bat` -> `tools/setup.ps1`: downloads PHP 8.4 (php.net "latest" zip), vc64web pinned to
  commit 469b63818d1a8f4d654fd3985b82aeb4e03fabba (skips its doc/ folder: long paths), removes
  vc64web's analytics script, copies ROMs from the local VICE install (fallback: VICE's GitHub mirror).
  Not yet tested on Windows.
- `start.bat`: PHP built-in server on port 8064, router `site/router.php`.
- Routes: `/` home, `/c64` emulator page, `/book/` = docs/, `/emu/` = runtime/vc64web,
  `/roms/` = runtime/roms, `/api/*` = site/lib/api.php.
- C64 page talks to vc64web directly through the same-origin iframe: `wasm_loadfile` (ROMs),
  `wasm_reset`, `wasm_peek`/`wasm_poke`, `wasm_auto_type`. Submit copies memory from TXTTAB ($2B)
  to VARTAB ($2D) into a PRG. Run/Load resets, pokes the PRG back, sets $2D/$2F/$31, types run/list.
- Tested end to end in headless Chrome: boot to READY, keyboard typing, Submit -> version 1 with
  correct listing, NEW, Run -> program runs.
- Gotchas found: the standard character ROM is chargen-901225-01 (906143-02 is the Japanese one);
  typed capitals arrive as Shift+letter = C64 graphics, so Caps Lock must be off and auto_type text
  must be lowercase; headless tests need ~110 ms key holds.
- Exercise list: `site/exercises.json` (placeholder entries for now). Chapter 1 has no
  submittable programs (direct mode only).

## Decisions made

- **Language and machine:** Commodore 64 BASIC V2. Reference emulator is VICE; TheC64
  gets its own appendix. Cassette covered only via VICE's datasette (appendix).
- **Known limits, no loopholes:** the book teaches the machine's documented limits as firm rules
  (8 sprites, 2-letter names, 80-character lines) and works within them. No sidebars on tricks that
  break limits (sprite multiplexing, opening the borders, etc.). Fun for the editor, confusing for
  a learner who does best with rules that hold.
- **Simplify, never falsify:** every rule the book states must be literally true on a real C64.
  Leaving things out is fine; a simplified rule that is false is not. Example (from the editor's own
  schooling): DIM A(10) creates ELEVEN elements, 0 to 10, never ten. The book says so plainly, then
  adopts a stated convention (editor's decision): data in boxes 1..N; box 0 is mentioned briefly as
  existing and "saved for special jobs", not taught as a lesson. Never claim DIM A(10) = 10 elements.
- **Writing style:** for a young adult beginner; plain language at roughly an 11-12-year-old reading level, never
  childish (no mascots, no cartoons, no talking down). Short sentences.
- **Core mental model:** a shelf of labelled boxes, used for every idea from variables
  to arrays, sorting, files and lookup tables. Each idea also gets a video-game picture.
- **Lesson format (7 steps):** Goal, Picture, Try it, Predict, Why it works,
  Organize it, Exercises and quiz.
- **Recurring projects:** Spending Tracker (v0 menu skeleton, v1 DATA + arrays,
  v2 sequential file, v3a relative file, v3b relative file + lookup tables) and
  Story Engine (DATA-driven scenes, later sprite, tune and disk files). The student's
  own stories are never submitted; only the engine is.
- **Money:** stored as whole cents in floating-point variables (integer variables
  overflow past 32767).
- **Course site:** portable, runs from a USB stick. PHP built-in web server + SQLite,
  started from a batch file. No Apache/MySQL needed. Student data in `data/`, never in git.
- **Emulator in the browser:** start with vc64web (maintained WebAssembly port of
  VirtualC64). Programs are stored as PRG bytes plus a text listing (via VICE's `petcat`);
  "Run" loads a stored PRG into the emulator. A custom VICE WebAssembly build is a
  possible later option, not a starting point.

## Naming traps already caught in drafts

Check every BASIC example name for hidden keywords. Caught so far: SPEND (END),
COLOR (OR), COST (COS), MONEY (ON), TOTAL (TO), SCORE (OR), TIME (TI).

## Open questions (waiting on the editor)

See the last section of `book/plan.md`: example name (placeholder KAITO), second-language
support, answer keys, paper vs. site notebook, title, reference machine.

## Next steps

1. The editor reviews the plan doc and answers the open questions.
2. Draft Chapter 2 (Talking to the Computer).
3. Editor runs setup.bat/start.bat on Windows; fix whatever breaks.
4. Milestone 4: quizzes. Then 5: login, review page, Copy for Claude, progress page.
