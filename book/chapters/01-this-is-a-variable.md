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

::: good-to-know
Want to know a secret? Type `?` instead of the whole word `PRINT`, and you get the same thing, quicker.

Think of `PRINT` as a "what is?" command: you ask, and the C64 answers with what it is. So to ask "what is in A?", you can type:

```
? A
```

To make the answer more meaningful, add a word after it:

```
? A "APPLES."
```

The C64 answers ` 8 APPLES.` And if you use `?` inside a program, `LIST` shows it spelled out as `PRINT`, because to the C64 they're the same word.
:::

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

**Why it fails.** The C64 answers `?TYPE MISMATCH  ERROR`. Box A is a number box, and "HELLO" is not a number. The label tells the C64 what kind of box it is:

| Label looks like | Box holds | Example |
| --- | --- | --- |
| `A`, `PR`, `X1` | Any number, including decimals | `PR = 23.45` |
| `N$`, `PY$` | Text, up to 255 characters | `N$ = "KAITO"` |
| `C%`, `Q%` | Whole numbers only, from −32768 to 32767 | `C% = 3` |

You will not need the `%` kind until much later. It is here so the table is complete.

**Try it.** The same letter can label two different boxes:

```
A = 5
A$ = "MILLION DOLLARS"
PRINT A;A$
```

The C64 answers ` 5 MILLION DOLLARS`. A and A$ are two separate boxes, one holding coins and one holding a note. The dollar sign is part of the label, so they never get mixed up.

## Lesson 1.3 — The two-letter trap

**Goal:** Learn the C64's naming rules, including the strange ones.

**Try it:**

```
PRICE = 50
PRIZE = 3
PRINT PRICE
```

**Predict before you run the last line.** Most people expect 50. The C64 prints 3.

**Why.** The C64 only reads the **first two letters** of a variable name. To the computer, PRICE and PRIZE are both just PR: the same box. The second line quietly replaced the 50. Nothing warned you. Lesson 1.5 shows how to make sure it never happens to you.

**Prove it.** Ask the C64 what's in all three names:

```
? PRICE
? PRIZE
? PR
```

All three answer ` 3`. Three names, one box.

Picture it this way: the C64 makes its labels with a label maker that can only print **two letters**. You ask for a label that says PRICE, and the machine prints PR. Later you ask for PRIZE, and it prints PR again. Now the shelf has one box with the label PR, and both names lead to it.

## Lesson 1.4 — Words the C64 has already claimed

**Goal:** Know which names are taken, so you can pick names without worrying.

**Picture:** Usernames in an online game. When you sign up, some names are already taken, and the game won't let you have them. The C64 has about seventy words it has already claimed for itself: its commands and functions, like `PRINT`, `GOTO` and `RUN`. Programmers call them **reserved words**. Appendix E lists every one.

**Predict.** Will this work? Write down yes or no, then try it:

```
GOLD = 100
```

**Why it fails.** The C64 answers `?SYNTAX  ERROR`. When you press RETURN, the C64 reads your line looking for its own words, and it finds them even in the middle of a name. Hidden inside GOLD is GO, as in `GO TO`. The C64 sees GO and can't make sense of the rest.

The fix is easy: pick a name with no hidden word. `GLD = 100` works, and so does `GD = 100`.

Plenty of good names have a reserved word hiding inside:

| Name | Hidden word |
| --- | --- |
| GOLD | GO |
| LIFE | IF |
| SCORE | OR |
| MONEY | ON |
| TOTAL | TO |
| COST | COS |
| FRIEND | END |
| LENGTH | LEN |
| FORMAT | FOR |
| STATUS | ST |
| TIME | TI |

That list can make names feel like a minefield. They aren't. Three facts turn it into a map:

1. **Inside quotes, nothing is reserved.** `PRINT "GOLD, LIFE AND SCORE"` works perfectly. The C64 only hunts for its words outside quotes.
2. **You almost always find out right away.** A name with a reserved word inside usually stops with an error the moment you press RETURN, so you fix it and move on. (There's one sneaky exception, in the box below.)
3. **Two-letter names are safe, with just eight exceptions.** The C64 only reads the first two letters of a name anyway, and only eight pairs are taken:

| Taken pair | Why |
| --- | --- |
| IF, ON, OR, TO, GO, FN | They're reserved words themselves |
| ST, TI | They're the C64's own boxes (ST reports on disks and tapes; TI is its clock) |

Any other two letters can never contain a reserved word. HP, XP, GD, SC, PR: all safe.

::: good-to-know
Here's the sneaky one. A name like `TITLE$` starts with TI, so to the C64 it's `TI$`, the clock shown as hours, minutes and seconds. `TITLE$ = "MY GAME"` gives `?ILLEGAL QUANTITY  ERROR`, which at least warns you. But `TITLE$ = "120000"` gives no error at all: it quietly sets the clock to 12:00:00. Names that start with TI or ST are best avoided completely.
:::

The rules for names, all in one place:

- A name starts with a letter. After that, letters and digits are allowed.
- Only the first two characters count.
- A name must not contain a reserved word.
- Two-letter names are always safe, except IF, ON, OR, TO, GO, FN, ST and TI.

## Lesson 1.5 — Organize it: the variable dictionary

**Goal:** Start the habit that keeps every program in this book under control.

Because the C64 will not warn you when two names collide, you need a written list of every variable a program uses. This is your **variable dictionary**. Start a page in your programmer's notebook like this:

| Name | Kind | What it holds | Example |
| --- | --- | --- | --- |
| `A` | Number | Practice box from Lesson 1.1 | 8 |
| `N$` | Text | My name | KAITO |
| `PR` | Number | Price of one item, in dollars | 50 |

**Notebook rule 1:** Before you use a new variable, write it in the dictionary. If its first two letters match one already there, or it's one of the eight taken pairs, pick a different name. Short names are fine: the dictionary is where you write down what they mean.

When a box holds an amount, write its **unit** in the dictionary too. Is PR the price in dollars or in cents? The number 50 means something very different in each. Later in this book, money is always stored in cents, and the dictionary is where you say so.

::: good-to-know
In 1999, a spacecraft called the Mars Climate Orbiter was lost at Mars. One team's program measured thruster force in one unit, and another team's program read those numbers as a different unit. Every number was right. Nobody had written down which units they were in.
:::

## Exercises

1. **Type and predict.** Put your age into a variable and your favorite number into another. Before printing their sum, write down what it will be.
2. **Fix it.** This set of commands does not work. Find both problems, explain each in one sentence, and fix them: `MONEY = 40`, then `TOTAL = MONEY + 10`.
3. **Build it.** Using three variables (your name, a game you like, and how many hours you have played it), make the C64 print one sentence about you. Add all three to your variable dictionary first.

## Quiz

1. After `A = 5` and then `A = A * 2`, what does `PRINT A` show? (a) 5 (b) 7 (c) 10 (d) An error. **Answer: c**
2. What does `PRINT Q` show if Q was never used? (a) Nothing (b) 0 (c) `?SYNTAX  ERROR` (d) Q. **Answer: b**
3. Which variable can hold the word HELLO? (a) `H` (b) `H%` (c) `H$` (d) Any of them. **Answer: c**
4. Which of these names is always safe? (a) `GOLD` (b) `HP` (c) `IF` (d) `TITLE$`. **Answer: b**
5. A program uses COUNT and CODE. What goes wrong? (a) Nothing (b) They share one box, CO (c) CODE is a command (d) `?TYPE MISMATCH  ERROR`. **Answer: b**
