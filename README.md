# Thinking in C64 BASIC

A course that teaches Commodore 64 BASIC as a way to practice organized thinking.
Every chapter teaches one piece of the language together with one habit of mind
that keeps programs (and thoughts) in order.

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
| `docs/` | The built book (student edition) served by GitHub Pages |
| `site/` | The course site: router, API, pages, and the C64 page |
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

Coming later: quizzes, the review page, the progress page, and login.

## What never lives here

Student work, grades, and quiz results. Those stay in the local SQLite database
on your own machine (`data/`, excluded by `.gitignore`).
