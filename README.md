# Thinking in C64 BASIC

A course that teaches Commodore 64 BASIC as a way to practice organized thinking.
Every chapter teaches one piece of the language together with one habit of mind
that keeps programs (and thoughts) in order.

## What lives here

| Path | What it is |
| --- | --- |
| `book/chapters/` | The book, one Markdown file per chapter |
| `docs/` | The built book (student edition) served by GitHub Pages |
| `tools/` | The build: `python tools/build.py --student --pages` |
| `HANDOFF.md` | Running notes so each new working session knows the decisions made so far and what comes next |

Coming later: the portable course site (PHP + SQLite) with the
browser emulator, quizzes, and submissions.

## What never lives here

Student work, grades, and quiz results. Those stay in the local SQLite database
on your own machine (`data/`, excluded by `.gitignore`).
