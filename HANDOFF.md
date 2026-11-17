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

Conventions in chapter files:
- Plain fenced code block = something to type. Renders as a C64 screen.
- ` ```{.diagram} ` fenced block = a picture, not to be typed. Renders as a dashed box.
- Quiz answers written as `**Answer: x**` at the end of each question; the student build
  strips them.

## Decisions made

- **Language and machine:** Commodore 64 BASIC V2. Reference emulator is VICE; TheC64
  gets its own appendix. Cassette covered only via VICE's datasette (appendix).
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
3. Proof-of-concept: portable PHP + SQLite skeleton with vc64web page, Submit and Run.
