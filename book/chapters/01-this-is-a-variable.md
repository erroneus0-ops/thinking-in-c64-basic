# Chapter 1: This Is a Variable

In this chapter you type commands and press RETURN, and the C64 does them right away. This is called **direct mode**. You won't need line numbers until Chapter 2.

## Lesson 1.1 — Boxes with labels

**Goal:** Put a number into the computer's memory and get it back.

**Picture:** Imagine a shelf in a garage or a storeroom. On it sits a row of boxes. Each box has a label stuck on the front, so you can find it again without opening every box. Each box holds one thing. A labelled box on the shelf is called a **variable**. The computer's memory is a very long shelf with thousands of these boxes.

If you play video games, you already know variables. Your coin counter is a box labelled COINS. Every time you pick up a coin, the game opens that box, adds one, and puts the new number back.

```{.diagram}
     A           B           C          <- labels
  +-----+     +-----+     +-----+
  |  7  |     |  0  |     |  0  |       <- what is inside
  +-----+     +-----+     +-----+
=======================================  <- the shelf
```

**Try it.** Type each line and press RETURN after it:

```
A = 7
PRINT A
```

The C64 answers `  7 `. You put 7 into the box labelled A, then asked to see what was inside.

**Predict.** Before typing the next lines, write down what you think the C64 will show. Then try it.

```
A = A + 1
PRINT A
PRINT B
```

**Why it works.** The `=` sign does not mean "is equal to" here. It means "put into." `A = A + 1` means: look in box A, add one, and put the answer back in box A. So A now holds 8. Box B was never filled, so it holds 0. On the C64, an empty number box always starts at 0.

That is exactly the coin counter from a game. `A = A + 1` is picking up one coin.

You may have noticed a space before each number. The C64 leaves room in front of every number for a minus sign, even when there isn't one.

## Lesson 1.2 — Numbers and words

**Goal:** Store words as well as numbers.

**Try it:**

```
N$ = "KAITO"
PRINT N$
PRINT "MY NAME IS ";N$
```

A label that ends in a dollar sign holds **text** (programmers call text a *string*). The text goes inside quotation marks. The semicolon in the last line glues two things together on the screen.

Think of two kinds of box on the shelf. A **coin box** holds amounts you can count and add. A **note box** holds a piece of paper with writing on it. You can't add two notes together the way you add coins, and you can't put a note in a coin box.

**Predict, then try:**

```
A = "HELLO"
```

**Why it fails.** The C64 answers `?TYPE MISMATCH ERROR`. Box A is a number box, and "HELLO" is not a number. The label tells the C64 what kind of box it is:

| Label looks like | Box holds | Example |
| --- | --- | --- |
| `A`, `PR`, `X1` | Any number, including decimals | `PR = 23.45` |
| `N$`, `PY$` | Text, up to 255 characters | `N$ = "KAITO"` |
| `C%`, `Q%` | Whole numbers only, from −32768 to 32767 | `C% = 3` |

You will not need the `%` kind until much later. It is here so the table is complete.

## Lesson 1.3 — The two-letter trap

**Goal:** Learn the C64's naming rules, including the strange ones.

**Try it:**

```
PRICE = 50
PRIZE = 3
PRINT PRICE
```

**Predict before you run the last line.** Most people expect 50. The C64 prints 3.

**Why.** The C64 only reads the **first two letters** of a variable name. To the computer, PRICE and PRIZE are both just PR: the same box. The second line quietly replaced the 50. Nothing warned you. That is why the next lesson matters.

Picture it this way: the C64 makes its labels with a label maker that can only print **two letters**. You ask for a label that says PRICE, and the machine prints PR. Later you ask for PRIZE, and it prints PR again. Now the shelf has one box with the label PR, and both names lead to it.

**One more trap. Try it:**

```
MONEY = 20
```

The C64 answers `?SYNTAX ERROR`. Hidden inside MONEY is the word ON, which is a BASIC command. The C64 sees the command and gets confused. The same thing happens with TOTAL (contains TO) and SCORE (contains OR). A few names are also taken by the computer itself: ST and TI, and anything beginning with them, such as TIME.

The rules, all in one place:

- A name starts with a letter.
- After that, letters and digits are allowed.
- Only the first two characters count.
- A name must not contain a BASIC command word.

## Lesson 1.4 — Organize it: the variable dictionary

**Goal:** Start the habit that keeps every program in this book under control.

Because the C64 will not warn you when two names collide, you need a written list of every variable a program uses. This is your **variable dictionary**. Start a page in your programmer's notebook like this:

| Name | Kind | What it holds | Example |
| --- | --- | --- | --- |
| `A` | Number | Practice box from Lesson 1.1 | 8 |
| `N$` | Text | My name | KAITO |
| `PR` | Number | Price of one item | 50 |

**Notebook rule 1:** Before you use a new variable, write it in the dictionary. If its first two letters match one already there, pick a different name.

## Exercises

1. **Type and predict.** Put your age into a variable and your favorite number into another. Before printing their sum, write down what it will be.
2. **Fix it.** This set of commands does not work. Find both problems, explain each in one sentence, and fix them: `MONEY = 40`, then `TOTAL = MONEY + 10`.
3. **Build it.** Using three variables (your name, a game you like, and how many hours you have played it), make the C64 print one sentence about you. Add all three to your variable dictionary first.

## Quiz

1. After `A = 5` and then `A = A * 2`, what does `PRINT A` show? (a) 5 (b) 7 (c) 10 (d) An error. **Answer: c**
2. What does `PRINT Q` show if Q was never used? (a) Nothing (b) 0 (c) `?SYNTAX ERROR` (d) Q. **Answer: b**
3. Which variable can hold the word HELLO? (a) `H` (b) `H%` (c) `H$` (d) Any of them. **Answer: c**
4. Why does `SCORE = 10` fail? (a) Names cannot be five letters (b) It contains the command word OR (c) Numbers must be decimals (d) S is reserved. **Answer: b**
5. A program uses COUNT and CODE. What goes wrong? (a) Nothing (b) They share one box, CO (c) CODE is a command (d) `?TYPE MISMATCH ERROR`. **Answer: b**
