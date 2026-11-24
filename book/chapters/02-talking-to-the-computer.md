# Chapter 2: Talking to the Computer

In Chapter 1, the C64 did each thing the moment you pressed RETURN. Now you'll learn to give it a list of steps to do later, in order, as many times as you like. That list is a **program**.

## Lesson 2.1 — Now or later

**Goal:** Tell the C64 to do something now, or save it for later.

**Picture:** A recipe card. Reading a recipe card doesn't cook anything. You write the steps down first, then follow them when it's time to cook. A video game level works the same way: the level is built in advance, and it plays out when you press Start.

**Try it.** Type this and press RETURN:

```
PRINT "GAME ON"
```

The C64 prints `GAME ON` straight away. That's **direct mode**, the way you worked in Chapter 1.

Now type this, with a number in front, and press RETURN:

```
10 PRINT "GAME ON"
```

**Predict.** Before you look, write down what you think happened.

**Why it works.** Nothing was printed. The number at the start told the C64: don't do this now, *store* it as line 10 of a program. That's **program mode**. To follow the stored steps, type:

```
RUN
```

Now `GAME ON` appears. To see the stored program, type:

```
LIST
```

## Lesson 2.2 — Lines know their places

**Goal:** Understand how line numbers keep a program in order.

**Try it.** Type these three lines in this exact order:

```
NEW
30 PRINT "FINISH LINE"
10 PRINT "START"
20 PRINT "HALFWAY"
```

`NEW` erases any program already stored, so you start clean.

**Predict.** You typed 30, then 10, then 20. What order will `LIST` show? What will `RUN` print? Write both down, then try them.

**Why it works.** The C64 files every line by its number, no matter what order you typed it in, like index cards sorted in a box:

```{.diagram}
  You typed:            The C64 keeps:
  30 PRINT "FINISH LINE"      10 PRINT "START"
  10 PRINT "START"        ->  20 PRINT "HALFWAY"
  20 PRINT "HALFWAY"          30 PRINT "FINISH LINE"
```

`RUN` always starts at the lowest number and works upward.

::: good-to-know
`PRINT` on its own, with nothing after it, prints an empty line. It's the easy way to put a gap between lines of output, so a screen doesn't look crowded.
:::

Notice the gaps: 10, 20, 30, not 1, 2, 3. If you later need a step between START and HALFWAY, there's room for it:

```
15 PRINT "QUARTER WAY"
```

`LIST` it and see where it went. Line numbers can be anything from 0 to 63999, so there's plenty of room.

::: good-to-know
Some later versions of BASIC have a command that renumbers a whole program for you. The C64's BASIC doesn't. If you number by ones and run out of room, you have to retype lines. Numbering by tens is how C64 programmers avoid that.
:::

## Lesson 2.3 — Changing your mind

**Goal:** Replace, remove, and look at parts of a program.

**Try it.** With the four-line program from Lesson 2.2 still stored, type:

```
20 PRINT "HALFWAY THERE!"
```

**Predict,** then `LIST` it.

**Why it works.** A line with a number that already exists **replaces** the old line. The C64 keeps only one line 20.

Now type just the number, and press RETURN:

```
15
```

`LIST` again. Line 15 is gone. A line number with nothing after it **removes** that line.

When programs get long, you won't want to see all of it at once. `LIST` can show part of a program:

| You type | The C64 shows |
| --- | --- |
| `LIST` | Every line |
| `LIST 20` | Only line 20 |
| `LIST 10-20` | Lines 10 through 20 |
| `LIST -20` | Everything up to line 20 |
| `LIST 20-` | Line 20 and everything after it |

`RUN` can start partway through, too: `RUN 20` starts the program at line 20 instead of at the beginning.

And `NEW` erases the whole program. There's no undo, so be sure before you use it.

## Lesson 2.4 — Fixing a line on the screen

**Goal:** Fix a mistake without retyping the whole line.

**Picture:** You might think of the C64's screen as a web form: you type in a box, then press Submit. It is, with one twist. The *whole screen* is the form, and every line on it has its own invisible Submit button. RETURN submits whichever line the cursor is on, not just the one you typed last.

**Try it.** Type this program, mistake included:

```
NEW
10 PRINT "TODAY'S TARGET:"
20 PRITN "500 POINTS"
30 PRINT "LET'S GO"
RUN
```

The C64 prints the first line, then stops with `?SYNTAX  ERROR IN 20`. Helpfully, it tells you which line has the problem. (Yes, the C64 really does print two spaces before the word ERROR.)

**Why it works.** `PRITN` isn't a word the C64 knows: the last two letters are swapped. You could fix it by retyping all of line 20. But there's a faster way, because the C64 lets you edit anything on the screen:

1. Type `LIST` so line 20 is on the screen.
2. Use the **arrow keys** to move the cursor up to line 20, and right until it's on the `T` of `PRITN`.
3. Type `NT`. Each letter you type replaces the one under the cursor, so `TN` becomes `NT`, and the line reads `20 PRINT "500 POINTS"`.
4. Press RETURN while the cursor is anywhere on that line. That's the line's Submit button.

When you press RETURN, the C64 reads the whole line from the screen and stores it, exactly as if you had typed it fresh. `LIST` and `RUN` to check.

**Making room.** Typing over only replaces letters. When a letter is *missing*, you need room for it. Put the cursor where the missing letter belongs and press SHIFT + INST/DEL. That's **INSERT**: everything from the cursor onward slides one place to the right, leaving a space. Type the missing letter into the gap, then press RETURN. On a PC keyboard, use the **Insert** key, or **Shift + Backspace**.

For example, if line 20 said `20 PRIT "500 POINTS"`, you'd put the cursor on the `T`, press INSERT once, and type `N`.

::: good-to-know
On the course site's C64 page, holding **Shift** and clicking on the C64 screen moves the cursor straight to where you clicked, instead of using the arrow keys.
:::

::: good-to-know
To clear the screen, hold SHIFT and press **CLR/HOME**. On a PC keyboard, that's **Shift + Home**. (On many laptops, Home is **Fn + Left Arrow**, so it's Shift + Fn + Left Arrow. The course site's C64 page also has a Clear screen button right under the screen.) CLR/HOME without SHIFT just moves the cursor to the top left corner, without erasing anything.

Clearing the screen never touches your program: type `LIST` and it's all still there. (If you've used other versions of BASIC, you might reach for `CLS`. The C64 doesn't have it.)
:::

::: good-to-know
Here's how C64 programmers clear the screen from *inside* a program. Type a line up to the opening quote, then press SHIFT + CLR/HOME:

```
10 PRINT "{clr}ROUND 1"
```

Inside quotes, SHIFT + CLR/HOME doesn't clear anything. Instead, it types the clear-screen code into your text, and the C64 shows it as a **reversed heart**. When the program runs, PRINT sends that code, the screen clears, and then ROUND 1 appears. This book writes the reversed heart as `{clr}`, because a heart is hard to print on paper.
:::

::: good-to-know
A program line can fill two rows of the screen, but keep it **shorter than 80 characters**. When you type the 80th character, the cursor jumps down to a fresh row, and pressing RETURN then enters that empty row instead of your line, so your line is never stored. Long lines are also hard to read, so this book keeps them short.
:::

## Lesson 2.5 — Organize it: plan, then number

**Goal:** Start every program on paper, not on the keyboard.

A program is a list of steps in order. Before you type, write the steps in your notebook in plain words, one per line, the way you'd write a recipe. Then give each step a line number, counting by tens.

| Step in plain words | Line |
| --- | --- |
| Show a title | 10 |
| Show today's goal | 20 |
| Show a cheer for reaching it | 30 |

Now the typing is just copying, and the thinking is already done.

**Notebook rule 2:** Plan the steps on paper first, in order. Number the lines by tens, so there's always room to add a step later.

## Exercises

Second time through? Find a different answer that still works, then compare it with your first.

1. **Predict the order.** Type `NEW`, then these lines in this order: `30 PRINT "BLUE"`, `10 PRINT "RED"`, `40 PRINT "VIOLET"`, `20 PRINT "GREEN"`. Before typing `LIST` and `RUN`, write down what each will show.
2. **Fix it two ways.** Type the TODAY'S TARGET program from Lesson 2.4. Fix line 20 once by retyping the whole line, then break it again and fix it with the screen editor. Which way was faster?
3. **Build it.** Plan a short "game over" screen on paper: a title, your final score, and a message, one per line, using variables from your variable dictionary. Number the lines by tens, type it, and run it. Then add a new line between the score and the message *without* retyping anything else.

## Quiz

1. You type `20 PRINT "SAVED"` and press RETURN. What happens? (a) SAVED appears (b) The line is stored and nothing is printed (c) `?SYNTAX  ERROR` (d) The program runs. **Answer: b**
2. You type lines 60, then 30, then 50. What does `LIST` show first? (a) Line 60 (b) Line 50 (c) Whichever you typed last (d) Line 30. **Answer: d**
3. What does typing `30` by itself and pressing RETURN do? (a) Removes line 30 (b) Runs line 30 (c) Lists line 30 (d) Nothing. **Answer: a**
4. Why number lines 10, 20, 30 instead of 1, 2, 3? (a) It runs faster (b) The C64 requires it (c) It leaves room to add lines in between (d) It saves memory. **Answer: c**
5. Which command shows only lines 20 through 40? (a) `LIST 20-40` (b) `RUN 20` (c) `LIST 40` (d) `LIST -20`. **Answer: a**
