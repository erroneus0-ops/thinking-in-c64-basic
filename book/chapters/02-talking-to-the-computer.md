# Chapter 2: Talking to the Computer

In Chapter 1, the C64 did each thing the moment you pressed RETURN. Now you'll learn to give it a list of steps to do later, in order, as many times as you like. That list is a **program**.

## Lesson 2.1 — Now or later

**Goal:** Tell the C64 to do something now, or save it for later.

**Picture:** A recipe card. Reading a recipe card doesn't cook anything. You write the steps down first, then follow them when it's time to cook. A video game level works the same way: the level is built in advance, and it plays out when you press Start.

**Try it.** Type this and press RETURN:

```
PRINT "HELLO"
```

The C64 prints `HELLO` straight away. That's **direct mode**, the way you worked in Chapter 1.

Now type this, with a number in front, and press RETURN:

```
10 PRINT "HELLO"
```

**Predict.** Before you look, write down what you think happened.

**Why it works.** Nothing was printed. The number at the start told the C64: don't do this now, *store* it as line 10 of a program. That's **program mode**. To follow the stored steps, type:

```
RUN
```

Now `HELLO` appears. To see the stored program, type:

```
LIST
```

## Lesson 2.2 — Lines know their places

**Goal:** Understand how line numbers keep a program in order.

**Try it.** Type these three lines in this exact order:

```
NEW
30 PRINT "THIRD"
10 PRINT "FIRST"
20 PRINT "SECOND"
```

`NEW` erases any program already stored, so you start clean.

**Predict.** You typed 30, then 10, then 20. What order will `LIST` show? What will `RUN` print? Write both down, then try them.

**Why it works.** The C64 files every line by its number, no matter what order you typed it in, like index cards sorted in a box:

```{.diagram}
  You typed:            The C64 keeps:
  30 PRINT "THIRD"      10 PRINT "FIRST"
  10 PRINT "FIRST"  ->  20 PRINT "SECOND"
  20 PRINT "SECOND"     30 PRINT "THIRD"
```

`RUN` always starts at the lowest number and works upward.

Notice the gaps: 10, 20, 30, not 1, 2, 3. If you later need a step between FIRST and SECOND, there's room for it:

```
15 PRINT "ONE AND A HALF"
```

`LIST` it and see where it went. Line numbers can be anything from 0 to 63999, so there's plenty of room.

::: good-to-know
Some later versions of BASIC have a command that renumbers a whole program for you. The C64's BASIC doesn't. If you number by ones and run out of room, you have to retype lines. Numbering by tens is how C64 programmers avoid that.
:::

## Lesson 2.3 — Changing your mind

**Goal:** Replace, remove, and look at parts of a program.

**Try it.** With the four-line program from Lesson 2.2 still stored, type:

```
20 PRINT "SECOND, CHANGED"
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

**Try it.** Type this program, mistake included:

```
NEW
10 PRINT "MY FAVORITE GAME IS"
20 PRNT "CHESS"
30 PRINT "I PLAY IT A LOT"
RUN
```

The C64 prints the first line, then stops with `?SYNTAX  ERROR IN 20`. Helpfully, it tells you which line has the problem. (Yes, the C64 really does print two spaces before the word ERROR.)

**Why it works.** `PRNT` isn't a word the C64 knows. You could fix it by retyping all of line 20. But there's a faster way, because the C64 lets you edit anything on the screen:

1. Type `LIST` so line 20 is on the screen.
2. Use the **arrow keys** to move the cursor up to line 20, and right until it's on the `N` of `PRNT`.
3. Type `INT`. Each letter you type replaces the one under the cursor, so `N`, `T` and the space become `I`, `N` and `T`. The line now reads `20 PRINT"CHESS"`. The space is gone, but that's fine: the C64 doesn't need spaces between words.
4. Press RETURN while the cursor is anywhere on that line.

When you press RETURN, the C64 reads the whole line from the screen and stores it, exactly as if you had typed it fresh. `LIST` and `RUN` to check.

::: good-to-know
A single program line can be at most 80 characters, which is two rows of the screen. Long lines are also hard to read, so this book keeps them short.
:::

## Lesson 2.5 — Organize it: plan, then number

**Goal:** Start every program on paper, not on the keyboard.

A program is a list of steps in order. Before you type, write the steps in your notebook in plain words, one per line, the way you'd write a recipe. Then give each step a line number, counting by tens.

| Step in plain words | Line |
| --- | --- |
| Show a title | 10 |
| Show my name | 20 |
| Show my favorite game | 30 |

Now the typing is just copying, and the thinking is already done.

**Notebook rule 2:** Plan the steps on paper first, in order. Number the lines by tens, so there's always room to add a step later.

## Exercises

1. **Predict the order.** Type `NEW`, then these lines in this order: `40 PRINT "D"`, `20 PRINT "B"`, `10 PRINT "A"`, `30 PRINT "C"`. Before typing `LIST` and `RUN`, write down what each will show.
2. **Fix it two ways.** Type the CHESS program from Lesson 2.4. Fix line 20 once by retyping the whole line, then break it again and fix it with the screen editor. Which way was faster?
3. **Build it.** Plan a program on paper that shows three facts about you, one per line, using variables from your variable dictionary. Number the lines by tens, type it, and run it. Then add a title line at the top *without* retyping anything else.

## Quiz

1. You type `10 PRINT "HI"` and press RETURN. What happens? (a) HI appears (b) The line is stored and nothing is printed (c) `?SYNTAX  ERROR` (d) The program runs. **Answer: b**
2. You type lines 30, then 10, then 20. What does `LIST` show first? (a) Line 30 (b) Line 10 (c) Whichever you typed last (d) Line 20. **Answer: b**
3. What does typing `20` by itself and pressing RETURN do? (a) Runs line 20 (b) Lists line 20 (c) Removes line 20 (d) Nothing. **Answer: c**
4. Why number lines 10, 20, 30 instead of 1, 2, 3? (a) The C64 requires it (b) It leaves room to add lines in between (c) It runs faster (d) It saves memory. **Answer: b**
5. Which command erases the whole program? (a) `LIST` (b) `END` (c) `CLR` (d) `NEW`. **Answer: d**
