<!-- status: final -->
# Chapter 1: This Is a Variable

This chapter teaches two things. The first is the **variable**: how the C64 remembers numbers and words. The second is the C64's **rules** about variables. Some of those rules are strange, and sooner or later one of them will trip you up. That happens to every C64 programmer.

You don't need to memorize the rules now. Read them once, and remember that they're here. Later, when a name doesn't work or a number lands in the wrong place, come back to this chapter and check whether one of these rules explains it. Good programmers don't know everything. They know where to look.

In this chapter you type commands and press RETURN, and the C64 does them right away. This is called **direct mode**. You won't need line numbers until Chapter 2.

## Lesson 1.1 — Boxes with labels

**Goal:** Put a number into the computer's memory and get it back.

**Picture:** Picture a row of lockers in a hallway. Each locker has a name tag on the door, so you can find it again without opening every one. Each locker holds one thing. A labelled box like this is called a **variable**, and the computer's memory is a very long row of them: thousands of boxes, side by side on one shelf.

If you play video games, you already know variables. Your experience points are a box labelled XP. Every time you finish a quest, the game opens that box, adds your reward, and puts the new total back.

```{.diagram}
     X           Y           K          <- labels
  +-----+     +-----+     +-----+
  | 100 |     |  0  |     |  0  |       <- what is inside
  +-----+     +-----+     +-----+
=======================================  <- the shelf
```

**Try it.** Type each line and press RETURN after it:

```
X = 100
PRINT X
```

The C64 answers ` 100`. You put 100 into the box labelled X, then asked to see what was inside.

**Predict.** Before typing the next lines, write down what you think the C64 will show. Then try it.

```
X = X + 25
PRINT X
PRINT Y
```

**Why it works.** The `=` sign does not mean "is equal to" here. It means "put into." `X = X + 25` means: look in box X, add 25, and put the answer back in box X. So X now holds 125. Box Y was never filled, so it holds 0. On the C64, an empty number box always starts at 0.

That is exactly a quest reward: `X = X + 25` is 25 more experience points.

Notice the space before each number. The C64 leaves room in front of every number for a minus sign, even when there isn't one.

::: good-to-know
Want to know a secret? Type `?` instead of the whole word `PRINT`, and you get the same thing, quicker.

Think of `PRINT` as a "what is?" command: you ask, and the C64 answers with what it is. So to ask "what is in X?", you can type:

```
? X
```

To make the answer more meaningful, add a word after it:

```
? X "XP"
```

The C64 answers ` 125 XP`. And if you use `?` inside a program, `LIST` shows it spelled out as `PRINT`, because to the C64 they're the same word.
:::

## Lesson 1.2 — Three kinds of boxes

**Goal:** Learn the three kinds of boxes, and prove they're different.

**Picture:** Not every box can hold everything. A coin jar holds amounts you can count and add. An envelope holds a written message. You can't add two messages together the way you add coins, and you can't drop a message into a coin jar and expect it to count. The kind of thing a box can hold is called its **data type**.

**Try it.** The same letter can label three different boxes:

```
G = 250
G$ = "GEMS FOUND"
G% = 7
PRINT G;G$;G%
```

**Predict** what the last line will show before you press RETURN.

**Why it works.** The C64 answers ` 250 GEMS FOUND 7`. There are three separate boxes here, all labelled G. The symbol at the end of a label is part of the label, and it tells the C64 what kind of box it is:

| Label looks like | Data type | Holds | Example |
| --- | --- | --- | --- |
| `G`, `SC`, `X1` | Number | Any number, including decimals | `G = 12.5` |
| `G$`, `N$` | Text (a **string**) | Letters, digits and symbols, up to 255 of them, in quotes | `G$ = "GEMS FOUND"` |
| `G%`, `L%` | Whole number | Whole numbers only, from −32768 to 32767 | `G% = 7` |

(Programmers in a wide variety of languages call whole numbers like these **signed integers**. More on that later in this book!)

**Mixing words and boxes.** The semicolon glues things together on one row, and it can glue words in quotes to boxes:

```
S = 12
PRINT "LEVEL";S;"CLEARED"
N$ = "NOVA"
PRINT N$;" SCORED";S;"STARS"
```

The C64 answers `LEVEL 12 CLEARED` and `NOVA SCORED 12 STARS`. Look closely at the spaces. A number brings its own space on each side, but words don't. That's why `" SCORED"` starts with a space inside its quotes: without it, you'd get NOVASCORED.

**Predict, then try:**

```
G = "GEMS"
```

The C64 answers `?TYPE MISMATCH  ERROR`. You tried to put a message into a number box. "Type mismatch" means the data type of the thing doesn't match the data type of the box.

**Prove it.** A whole-number box is fussy. Try these:

```
G% = 9.99
? G%
G% = 50000
```

The first answer is ` 9`. The whole-number box doesn't round 9.99 up to 10: it simply drops everything after the decimal point. And 50000 gives `?ILLEGAL QUANTITY  ERROR`, because it's too big to fit.

::: good-to-know
If the whole-number box is so fussy, why have it at all? It takes up less room in memory. That won't matter for single boxes, but much later in this book you'll build long rows of boxes, and there it adds up.
:::

## Lesson 1.3 — The two-letter trap

**Goal:** Learn the C64's naming rules, including the strange ones.

**Try it:**

```
SHIELD = 80
SHOTS = 5
PRINT SHIELD
```

**Predict before you run the last line.** Most people expect 80.

**Why.** The C64 prints 5. It only reads the **first two letters** of a variable name. To the computer, SHIELD and SHOTS are both just SH: the same box. The second line quietly replaced the 80. Nothing warned you. Lesson 1.5 shows how to make sure it never happens to you.

**Prove it.** Ask the C64 what's in all three names:

```
? SHIELD
? SHOTS
? SH
```

All three answer ` 5`. Three names, one box.

Picture it this way: the C64 makes its labels with a label maker that can only print **two letters**. You ask for a label that says SHIELD, and the machine prints SH. Later you ask for SHOTS, and it prints SH again. Now the shelf has one box with the label SH, and both names lead to it.

## Lesson 1.4 — Words the C64 has already claimed

**Goal:** Know which names are taken, so you can pick names without worrying.

**Picture:** Usernames in an online game. When you sign up, some names are already taken, and the game won't let you have them. The C64 has about seventy words it has already claimed for itself: its commands and functions, like `PRINT`, `GOTO` and `RUN`. Programmers call them **reserved words**. Appendix E will list every one.

**Predict.** Will this work? Write down yes or no, then try it:

```
FORTUNE = 7
```

**Why it fails.** The C64 answers `?SYNTAX  ERROR`. When you press RETURN, the C64 reads your line looking for its own words, and it finds them even in the middle of a name. Hidden inside FORTUNE is FOR, as in `FOR ... NEXT`. The C64 sees FOR and can't make sense of the rest.

The fix is easy: pick a name with no hidden word. `LUCK = 7` works, and so does `LK = 7`.

Plenty of good names have a reserved word hiding inside:

| Name | Hidden word |
| --- | --- |
| FORTUNE | FOR |
| DEFENSE | DEF |
| VALUE | VAL |
| TOKEN | TO |
| DIFFICULTY | IF |
| GOLD | GO |
| POINTS | INT |
| BONUS | ON |
| SCORE | OR |
| FRIEND | END |
| STATUS | ST |
| TIME | TI |

That list can make names feel like a minefield. They aren't. Three facts turn it into a map:

1. **Inside quotes, nothing is reserved.** `PRINT "FORTUNE, DEFENSE AND VALUE"` works perfectly. The C64 only hunts for its words outside quotes.
2. **You almost always find out right away.** A name with a reserved word inside usually stops with an error the moment you press RETURN, so you fix it and move on. (There's one sneaky exception, in the box below.)
3. **Two-letter names are safe, with just eight exceptions.** The C64 only reads the first two letters of a name anyway, and only eight pairs are taken:

| Taken pair | Why |
| --- | --- |
| IF, ON, OR, TO, GO, FN | They're reserved words themselves |
| ST, TI | They're the C64's own boxes (ST reports on disks and tapes; TI is its clock) |

Any other two letters can never contain a reserved word. XP, HP, SH, LK, GM: all safe.

::: good-to-know
Here's the sneaky one. A name like `TITLE$` starts with TI, so to the C64 it's `TI$`, the clock shown as hours, minutes and seconds. `TITLE$ = "MY GAME"` gives `?ILLEGAL QUANTITY  ERROR`, which at least warns you. But `TITLE$ = "120000"` gives no error at all: it quietly sets the clock to 12:00:00. Names that start with TI or ST are best avoided completely.
:::

The rules for names, all in one place:

- A name starts with a letter. After that, letters and digits are allowed.
- Only the first two characters count, plus the `$` or `%` that sets the data type.
- A name must not contain a reserved word.
- Two-letter names are always safe, except IF, ON, OR, TO, GO, FN, ST and TI.

## Lesson 1.5 — Organize it: the variable dictionary

**Goal:** Start the habit that keeps every program in this book under control.

Because the C64 will not warn you when two names collide, you need a written list of every variable a program uses. This is your **variable dictionary**. Start a page in your programmer's notebook like this (any paper notebook works, and until you have one, a sheet of paper will do):

| Name | Data type | What it holds | Example |
| --- | --- | --- | --- |
| `X` | Number | Experience points earned | 125 |
| `N$` | Text | Player name | NOVA |
| `CS` | Number | Cash, in dollars | 75 |

**Notebook rule 1:** Before you use a new variable, write it in the dictionary. If its first two letters match one already there, or it's one of the eight taken pairs, pick a different name. Short names are fine: the dictionary is where you write down what they mean.

When a box holds an amount, write its **unit** in the dictionary too. Is CS the cash in dollars or in cents? The number 75 means something very different in each. Later in this book, money is always stored in cents, and the dictionary is where you say so.

::: good-to-know
In 1999, a spacecraft called the Mars Climate Orbiter was lost at Mars. One team's program measured thruster force in one unit, and another team's program read those numbers as a different unit. Every number was right. Nobody had written down which units they were in.
:::

## Exercises

1. **Type and predict.** Put the points you scored in two rounds of a game into two variables. Before printing their total, write down what it will be.
2. **Fix it.** These commands don't work. Find both problems, explain each in one sentence, and fix them: `ARMOR = 30`, then `ENDURANCE = ARMOR * 2`.
3. **Build it.** Use three variables: the name of a place in a game you like, how many treasures are hidden there, and the name of the best treasure. Make the C64 print one sentence about it, mixing words and boxes the way Lesson 1.2 shows. Add all three to your variable dictionary first, with their data types.

## Quiz

1. After `X = 4` and then `X = X * 5`, what does `PRINT X` show? (a) 4 (b) 9 (c) 20 (d) An error. **Answer: c**
2. After `G% = 9.99`, what does `PRINT G%` show? (a) 9.99 (b) 10 (c) 9 (d) An error. **Answer: c**
3. Which variable can hold the words GOOD JOB? (a) `W` (b) `W%` (c) `W$` (d) Any of them. **Answer: c**
4. Which of these names is always safe? (a) `DEFENSE` (b) `HP` (c) `TO` (d) `STARS`. **Answer: b**
5. A program uses MAGIC and MANA. What goes wrong? (a) Nothing (b) They share one box, MA (c) MANA is a command (d) `?TYPE MISMATCH  ERROR`. **Answer: b**
