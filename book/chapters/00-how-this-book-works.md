<!-- status: final -->
# How This Book Works

This book teaches you to program the Commodore 64. It also teaches something bigger: how to plan, how to keep things in order, and how to break a big job into small ones. Programmers call that *organized thinking*. The C64 is a good place to learn it, because its BASIC gives you almost no help. Any order in your program has to come from you.

## Your pace

This book is **self-paced**. There's no deadline and no hurry. Go back, re-read, and practice any lesson as often as you like, for as long as you like, until it feels comfortable. Then move on when you're ready.

## What you need

- **The course site:** the book, the C64 page, and Chapter work. (VICE on your computer works too.)
- **A paper notebook and a pencil.** This is your **programmer's notebook**, where you'll draw tables and maps before you type. Any notebook works, and until you have one, a sheet of paper will do.
- **About thirty minutes.** Every lesson fits in one sitting.

## Reading the code

Anything shown on a dark blue screen like this is something to type:

```
PRINT "HELLO"
```

The little **↵** key at the end of the line means: press RETURN (Enter on a PC keyboard). The C64 does nothing with a line until you do. You don't type the symbol itself.

## How every lesson goes

Every lesson has the same seven steps, so you always know where you are:

1. **Goal**: what you will be able to do by the end.
2. **Picture**: a drawing of the idea.
3. **Try it**: type something short and run it.
4. **Predict**: change one thing, write down what you think will happen, then run it.
5. **Why it works**: a short explanation.
6. **Organize it**: one habit to add to your notebook.
7. **Exercises and quiz**: practice, then five quick questions.

Getting a prediction wrong is not a failure. It's how you find out what the computer really does. Error messages are normal too. Every chapter makes at least one on purpose.

## Working through a chapter

Each chapter only needs to be worked through **once**, in this order:

1. **Read each lesson and try every example** on the C64. Many people keep the book and the C64 side by side on the screen.
2. **After each lesson, write your notes** on the Chapter work page: explain the big idea in your own words, and say what surprised you, confused you, or dragged.
3. **Do the exercises.** When an exercise asks for a program, choose it in the Exercise list on the C64 page and press **Save to a new slot**, so it's kept. Every save goes into a new slot, and nothing is ever overwritten.
4. **Take the quiz last.**

That's the whole chapter. If something in it is fixed or improved later, you'll be told what changed, but you won't be asked to work through it again. You can always come back on your own, though: retake a quiz to raise your score, or play with the examples to see what else they do. Every attempt is kept. Coming back is never required, and always welcome.

## Tools that help

- **Study view**, on the course site's home page, puts the C64 and the book side by side on one screen, with the workbook (exercises, quiz and notes) sliding in from the right when you need it.
- **Show variables**, under the C64 screen, shows every box the C64 knows about, sorted into cabinets.
- **Shift-click** on the C64 screen moves the cursor there.
- **Insert** (or **Shift + Backspace**) makes room for a missing letter. It works like the text editing you're used to on a PC or phone: it makes room instead of typing over.
- **Clear screen**, under the C64 screen, wipes the screen without touching your program.
- **The quick tour**, linked at the top of the book's web page, shows all of this in a few slides.
- **The [Reference](%REF%)** is a separate volume for looking things up: every keyword, abbreviation and error message of C64 BASIC, in plain, exact terms.
- **The save slots guide** walks through saving, loading and running your programs, step by step. It's linked next to the save button on the C64 page.

## Getting unstuck

Everyone gets stuck. When you do, try these in order:

1. **Look back.** Re-read the lesson you're on, and check Chapter 1's rules about names. Good programmers don't know everything; they know where to look.
2. **Ask an AI, the right way.** A free AI chatbot can usually help, if you ask well:
    - **Name the machine every time.** Start with "In Commodore 64 BASIC V2," because other versions of BASIC work differently.
    - **Give the exact line and the exact error,** not a description. For example: *In Commodore 64 BASIC V2, I typed `PRINT "LEVEL: "+L` and got `?TYPE MISMATCH  ERROR`. Why?*
    - **Ask for a hint first:** "Don't fix it for me, just tell me what's wrong." Then the discovery is still yours.
    - **Check every answer on the C64.** AIs often get C64 BASIC wrong. They may suggest `ELSE`, for example, which the C64 doesn't have. The C64 is always the final judge, and catching an AI's mistake counts as a discovery too.

## A note for the beta tester

This book is a **draft**, and you're its **beta tester**. Like a beta tester for a game, your job is to find the problems before anyone else does. If something confuses you, that's the book's fault, not yours, and you've just found something to fix. Several of the tools above exist because a beta tester asked for them.

## Exercises

1. **Make room.** Type `10 PRNT "READY"` and press RETURN. Now fix the missing letter *without* retyping the line: move the cursor onto the `N`, press **Insert**, type `I`, then press RETURN. `LIST` and `RUN` to check.
2. **Save, reset, load.** Save your program from exercise 1 to a slot (choose "Before you begin, exercise 2" in the Exercise list). Press **Reset the C64**, then use your slot's **Load** button to bring it back, and run it.
3. **Ask well.** Ask a free AI one question about something in this book, following the four steps in "Getting unstuck." Write down the question you asked, the hint you got, and whether the C64 agreed.

## Quiz

1. What does the ↵ at the end of a line of code mean? (a) Type the ↵ symbol (b) Press RETURN (c) The line continues on the next row (d) Nothing. **Answer: b**
2. You've typed a program you want to keep. What should you do before pressing Reset? (a) Type NEW (b) Clear the screen (c) Save it to a new slot (d) Nothing. **Answer: c**
3. A word in a line is missing a letter. What's the quickest fix? (a) Put the cursor where it belongs, press Insert, type the letter (b) Retype the whole line (c) Clear the screen (d) Type LIST. **Answer: a**
4. An AI tells you to use `ELSE`, and the C64 answers `?SYNTAX  ERROR`. Who's right? (a) The AI (b) Both (c) Neither (d) The C64. **Answer: d**
5. Where do your notes about each lesson go? (a) On the C64's screen (b) On the Chapter work page (c) In a save slot (d) In the book. **Answer: b**
