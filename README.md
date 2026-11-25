# Thinking in C64 BASIC

A course that teaches Commodore 64 BASIC as a way to practice organized thinking.
Every chapter teaches one piece of the language together with one habit of mind
that keeps programs (and thoughts) in order.

## Two parts

- **The book** is published on GitHub Pages: <https://erroneus0-ops.github.io/thinking-in-c64-basic/>,
  together with a quick tour of the course site and a step-by-step guide to save slots.
- **The course site** runs on your own computer. Everything it needs is in this repo, except the
  C64's ROMs: they're copyrighted, so they can't be published here. Setup copies them from your own
  [VICE](https://vice-emu.sourceforge.io/) installation. The site gives you a C64 in the browser
  (the vc64web emulator), a study view with the book and the C64 side by side, a workbook with
  exercises, quizzes and notes, save slots for your programs, and a live view of the C64's variables.

## Who it's for

A young adult beginner with no programming experience: bright, strong at spatial
reasoning, good at video games, and easily distracted. The writing is plain and
simple without ever being childish, and every idea is shown with an everyday picture
and a video-game picture.

## What lives here

| Path | What it is |
| --- | --- |
| `book/plan.md` | The book plan: premise, lesson format, mental models, outline, recurring projects, C64 traps |
| `book/chapters/` | The book, one Markdown file per chapter |
| `docs/` | What GitHub Pages serves: the built book, the quick tour, and the save slots guide |
| `site/` | The course site (runs locally): the C64, study view, workbook, save slots, and Editor's view |
| `setup.bat`, `start.bat` | One-time setup, and starting the course site |
| `tools/` | The book build (`python tools/build.py --student --pages`) and setup scripts |
| `HANDOFF.md` | Running notes so each new working session knows the decisions made so far and what comes next |

## Running the course site (Windows)

1. Install [VICE](https://vice-emu.sourceforge.io/) if it isn't already (setup copies the C64 ROMs from it).
2. Double-click **setup.bat** once. It downloads portable PHP and the vc64web emulator into `runtime/`.
3. Double-click **start.bat**. Your browser opens the course site; the window shows the address
   for a phone on the same Wi-Fi. Keep the window open while working.

When typing into the emulator, keep **Caps Lock off**: capital letters typed with Shift or Caps Lock
become C64 graphics characters, exactly as on a real C64.

On the home page you'll find the **study view** (the C64 and the book side by side, with the workbook
a click away), **Chapter work** (exercises, quizzes and notes), and the **Editor's view** of everyone's
progress. Sign-in is by name only: the site is meant for a household network, not the internet.

## What never lives here

- **Student work, notes, and quiz results.** Those stay in the local SQLite database on your own
  machine (`data/`, excluded by `.gitignore`).
- **The C64's ROMs.** They're copyrighted. Setup copies them from your own VICE installation into
  `runtime/` (also excluded by `.gitignore`).
