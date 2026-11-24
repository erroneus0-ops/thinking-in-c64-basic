# Chapter 3: Working Things Out

In this chapter the C64 becomes a calculator, then a dice roller. You'll learn how it does arithmetic, which part of a calculation it works out first, how to keep only the whole part of a number, and how to make it pick numbers at random. The chapter ends with a surprise about "random" that most people never notice.

## Lesson 3.1 — The C64 as a calculator

**Goal:** Do arithmetic with the C64, and meet its five arithmetic signs.

**Picture:** A game is always calculating behind the scenes: damage, bonuses, how much gold is left after you buy something. The C64 can do the same sums, and it shows you every one.

**Try it.** `?` works as a calculator. Type each line:

```
? 7+5
? 7-5
? 7*5
```

The C64 answers ` 12`, ` 2` and ` 35`. On a computer, **\*** means times, because the letter X would be confused with a variable called X.

**Predict.** What will these show? Write your answers down first.

```
? 7/2
? 2↑3
```

**Why it works.** The C64 answers ` 3.5` and ` 8`. The **/** sign means divided by, and the C64 keeps the decimal part. The **↑** sign means "to the power of": 2↑3 is 2 × 2 × 2, which is 8. On the course site's C64, type ↑ with the **^** key (Shift + 6 on most keyboards).

| Sign | Means | Example | Answer |
| --- | --- | --- | --- |
| `+` | plus | `7+5` | 12 |
| `-` | minus | `7-5` | 2 |
| `*` | times | `7*5` | 35 |
| `/` | divided by | `7/2` | 3.5 |
| `↑` | to the power of | `2↑3` | 8 |

**One more, on purpose:**

```
? 10/0
```

The C64 answers `?DIVISION BY ZERO  ERROR`. Nobody can split something into zero parts, not even a computer, so it stops and tells you.

## Lesson 3.2 — Which part goes first

**Goal:** Know the order in which the C64 works out a calculation, and control it.

**Picture:** A damage formula in a game: base damage, plus a bonus times a multiplier. Whether the bonus gets multiplied before or after it's added changes the result completely. The C64 always follows the same order, so you can predict it.

**Predict.** Write down your answer before you type it:

```
? 2+3*4
```

**Why it works.** The C64 answers ` 14`, not 20. It does the multiplying *first*: 3 times 4 is 12, then 2 plus 12 is 14. The order is always:

1. Anything in **parentheses** `( )`.
2. **Powers** (↑).
3. **Times and divided by** (`*` and `/`), from left to right.
4. **Plus and minus** (`+` and `-`), from left to right.

Parentheses let you choose:

```
? (2+3)*4
```

That's ` 20`: now the adding happens first. When in doubt, add parentheses. They never hurt, and they make your intention clear to anyone reading the line, including you, later.

**Prove it.** Try these, predicting each one first:

```
? 12/2*3
? 2+3↑2
```

The answers are ` 18` (12 divided by 2 is 6, then times 3, working left to right) and ` 11` (3↑2 is 9, then plus 2).

**Organize it.** Before you type a calculation, work it out on paper, following the order above. Then compare your answer with the C64's.

**Notebook rule 3:** Work it out on paper first. If your answer and the C64's disagree, one of you is wrong, and finding out which teaches you something either way.

## Lesson 3.3 — Keeping the whole part

**Goal:** Use `INT` to keep only the whole-number part of a number.

**Picture:** Splitting a treasure chest between players. Gems can't be cut in half, so everyone gets a whole number of gems, and whatever's left over stays in the chest.

**Try it:**

```
? INT(7.9)
```

The C64 answers ` 7`. `INT` keeps the whole part and throws away everything after the decimal point. It doesn't round 7.9 up to 8.

**Predict.** 100 gems, 3 players. How many does each player get, and how many are left over? Work it out on paper, then try it:

```
G = 100
P = 3
? INT(G/P)
? G-INT(G/P)*P
```

**Why it works.** The C64 answers ` 33` and ` 1`. `G/P` is 33.333…, and `INT` keeps 33: each player's share. Then `INT(G/P)*P` is the 99 gems handed out, so `G` minus that leaves 1 gem in the chest. That second line is the **remainder**, what's left over after an even split.

::: good-to-know
`INT` always goes *down* to the next whole number, and for a negative number, down means further from zero. So `INT(-2.5)` is −3, not −2. And to round to the *nearest* whole number instead, add a half first: `INT(2.5 + .5)` gives 3.
:::

## Lesson 3.4 — Rolling dice

**Goal:** Make the C64 pick random numbers, and turn them into dice rolls.

**Picture:** Every game with loot drops, critical hits or dice has a random number generator inside. The C64 has one too, called `RND`.

**Try it.** Type this a few times:

```
? RND(1)
```

Each time, you get a different number between 0 and 1, like ` .185564016`. It's never quite 1.

**Building a die.** A die needs a whole number from 1 to 6. Build it one step at a time, and work out each step's range on paper:

| Step | Gives a number from | Why |
| --- | --- | --- |
| `RND(1)` | 0 up to (but not) 1 | that's what RND gives |
| `RND(1)*6` | 0 up to (but not) 6 | six times bigger |
| `INT(RND(1)*6)` | 0 to 5, whole | INT drops the decimal part |
| `INT(RND(1)*6)+1` | 1 to 6, whole | one more, so it starts at 1 |

**Predict,** then roll the die a few times:

```
? INT(RND(1)*6)+1
```

Every answer is a whole number from 1 to 6. Change the 6 to 20, and you've built the 20-sided die from tabletop games.

## Lesson 3.5 — The secret of random

**Goal:** Find out what "random" really means on the C64.

**Predict.** Press **Reset the C64** on the course site (or turn your C64 off and on). Then type:

```
? RND(1)
```

Write down the number. Now reset again and type the same line. Before you press RETURN, predict: will the number be different this time?

**Why it happens.** It's exactly the same number, every time. The C64's random numbers aren't truly random. They come from a recipe: each number is worked out from the one before it. After a reset, the recipe always starts in the same place, so the "random" numbers always come out in the same order.

Remember the maze from the very first pages? Stop it and run it again, and you get a different maze, because the recipe carries on from where it was. But right after a reset, the first maze is always the same one.

**The fix.** To start the recipe somewhere different each time, mix in the C64's clock. `TI` counts time since the C64 was switched on, and it's almost never the same twice:

```
X = RND(-TI)
? RND(1)
```

A negative number inside `RND` tells it to restart the recipe from that number. Since `TI` is different every time, so is the starting point. Put `X = RND(-TI)` at the top of any program that should be different every run.

::: good-to-know
Repeatable "random" numbers aren't a flaw: game makers sometimes use them on purpose. When a game lets you type in a "seed" to get the same world as a friend, that's this same idea: the same starting point gives the same "random" world.
:::

## Exercises

1. **Rate a creature.** In creature-collecting games like Pokémon GO, each creature has three hidden stats, attack, defense and HP, each from 0 to 15. Its rating is the total out of 45, as a percentage. Put 13, 14 and 15 into `AT`, `DF` and `HP`. First predict what `? AT+DF+HP/45*100` shows, then type it, and explain why it's wrong. Fix it with parentheses, then use `INT` to round the rating to the nearest whole percent.
2. **Split the loot.** 250 gems, 4 players. Use variables and `INT` to print how many gems each player gets, and how many are left in the chest.
3. **Build it.** Write a program that rolls two dice and prints both rolls and their total, mixing words and boxes. Make sure it rolls differently after every reset. Submit it on the C64 page.

## Quiz

1. What does `? 2+3*4` show? (a) 20 (b) 14 (c) 24 (d) 9. **Answer: b**
2. What does `? INT(9.99)` show? (a) 10 (b) 9.99 (c) 9 (d) An error. **Answer: c**
3. Which gives a whole number from 1 to 6? (a) `RND(6)` (b) `INT(RND(1)*6)` (c) `RND(1)*6+1` (d) `INT(RND(1)*6)+1`. **Answer: d**
4. What happens with `? 10/0`? (a) It shows 0 (b) It shows 10 (c) `?DIVISION BY ZERO  ERROR` (d) The C64 resets. **Answer: c**
5. Right after a reset, `? RND(1)` gives… (a) the same number every time (b) a different number every time (c) always 0 (d) an error. **Answer: a**
