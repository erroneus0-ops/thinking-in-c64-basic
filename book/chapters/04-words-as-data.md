<!-- status: testing -->
# Chapter 4: Words as Data

Numbers aren't the only thing a program works with. Names, titles, messages and codes are information too, and the C64 can join them together, measure them and cut them into pieces. In this chapter you'll learn how, and you'll finish by inventing new creature names.

## Lesson 4.1 — Joining words

**Goal:** Join pieces of text together into one.

**Picture:** Snapping building blocks together. Two blocks become one longer block, and you can keep adding more.

**Try it:**

```
A$ = "GOLD"
B$ = "EN"
? A$+B$
```

The C64 answers `GOLDEN`. With text, the **+** sign doesn't add: it joins. Programmers call joining text **concatenation**, a long word for snapping blocks together.

You can join as many pieces as you like, including text in quotes:

```
? "SKY"+" "+"KNIGHT"
```

That's `SKY KNIGHT`. The space in the middle is a piece of text too, so it gets joined like any other.

**Predict, then try:**

```
? "SCORE: "+5
```

**Why it fails.** The C64 answers `?TYPE MISMATCH  ERROR`. You can join text to text, and add numbers to numbers, but `+` can't mix the two: it doesn't know whether you mean "join" or "add". (Lesson 4.4 shows how to turn a number into text, so it can be joined.)

## Lesson 4.2 — How long is a word?

**Goal:** Measure text with `LEN`, and use it to center a title.

**Picture:** Counting the tiles in a word game. Every letter is a tile, and so is every space.

**Try it:**

```
? LEN("DRAGON")
? LEN("GAME ON")
```

The C64 answers ` 6` and ` 7`. `LEN` counts the characters, and the space in GAME ON counts as one.

**Centering a title.** The C64's screen is 40 characters wide. To put a title in the middle, push it right by half of the space that's left over. `SPC(n)` prints n spaces:

```
T$ = "GAME OVER"
PRINT SPC(INT((40-LEN(T$))/2));T$
```

**Predict** how many spaces it will push the title along: GAME OVER is 9 characters, so 40 − 9 = 31 spaces are left, and half of that, rounded down with `INT`, is 15. The title lands in the middle of the screen, and it works for any title you put in `T$`.

## Lesson 4.3 — Taking pieces

**Goal:** Cut pieces out of text with `LEFT$`, `RIGHT$` and `MID$`.

**Picture:** A strip of letter tiles. You can take some tiles from the left end, some from the right end, or some from the middle.

**Try it:**

```
? LEFT$("DRAGONFIRE",6)
? RIGHT$("DRAGONFIRE",4)
```

The C64 answers `DRAGON` and `FIRE`. `LEFT$(text, n)` takes n characters from the left; `RIGHT$(text, n)` takes n from the right.

**Predict.** `MID$(text, start, n)` takes n characters starting at position `start`. What will this show?

```
? MID$("DRAGONFIRE",4,3)
```

**Why it works.** The answer is `GON`: starting at the 4th letter, the G, it takes 3 letters. Leave the last number out, and `MID$` takes everything to the end: `MID$("DRAGONFIRE",7)` gives `FIRE`.

| Function | Takes | Example | Answer |
| --- | --- | --- | --- |
| `LEFT$(T$,n)` | n characters from the left | `LEFT$("DRAGONFIRE",6)` | DRAGON |
| `RIGHT$(T$,n)` | n characters from the right | `RIGHT$("DRAGONFIRE",4)` | FIRE |
| `MID$(T$,s,n)` | n characters, starting at position s | `MID$("DRAGONFIRE",4,3)` | GON |

All three end in `$`, because what they give back is text.

## Lesson 4.4 — Numbers and words

**Goal:** Turn numbers into text and text into numbers, and learn to see exactly what's inside a piece of text.

**Try it.** `STR$` turns a number into text, so it can be joined:

```
L = 5
? "LEVEL "+STR$(L)
```

**Predict** exactly what will appear, including the spaces.

**Why it looks odd.** The C64 answers `LEVEL  5`, with two spaces. One came from `"LEVEL "`, but where did the other come from? Look inside:

```
? "[";STR$(42);"]"
? LEN(STR$(42))
```

The answers are `[ 42]` and ` 3`. `STR$` keeps the space the C64 always leaves in front of a positive number, for a minus sign. So `"LEVEL"+STR$(L)`, without the space after LEVEL, gives `LEVEL 5`.

**Organize it.** Text can hide things you can't see, like spaces at the start or end. When text looks wrong, wrap it in brackets to see exactly what's there, as above.

**Notebook rule 4:** When text looks wrong, print it between brackets. What's inside the brackets is exactly what's in the box.

**The other direction.** `VAL` turns text into a number:

```
? VAL("123")+1
? VAL("42 GEMS")
? VAL("GEMS")
```

The C64 answers ` 124`, ` 42` and ` 0`. `VAL` reads digits from the start of the text and stops at the first thing that isn't part of a number. If there are no digits at the start, it gives 0.

## Lesson 4.5 — Fusion names

**Goal:** Combine everything in this chapter to invent new creature names.

**Picture:** Fusing two creatures into one: the front half of one, the back half of the other.

**Try it.** Take the first half of one name and the last half of another:

```
A$ = "DRAGON"
B$ = "KITTEN"
? LEFT$(A$,INT(LEN(A$)/2))+RIGHT$(B$,INT(LEN(B$)/2))
```

**Predict** the fused name before you press RETURN. DRAGON has 6 letters, so its first half is 3 letters; KITTEN's last half is 3 letters too.

**Why it works.** The C64 answers `DRATEN`. `LEN` measures each name, dividing by 2 finds the half, `INT` keeps it a whole number, `LEFT$` and `RIGHT$` cut the pieces, and `+` snaps them together. Every tool from this chapter, in one line.

Now try your own. `A$ = "PHOENIX"` and `B$ = "TIGER"` make `PHOER`. Odd-length names work too, because `INT` rounds each half down. Swap the two names around, and you get a completely different creature.

## Exercises

1. **Join it.** Put two words into two text boxes, such as SKY and KNIGHT. Join them with a space in between, and print the result. Then print its `LEN`, and check that it counted the space.
2. **Fix it two ways.** `L = 5`, then `PRINT "LEVEL: "+L` gives an error. Explain why, then fix it once using a semicolon and once using `STR$`. Use brackets to check the spaces in your second fix.
3. **Build it: a clock.** In direct mode, set the C64's clock once with `TI$ = "093000"`. Then write a one-line program that prints `TI$` as hours, minutes and seconds with colons between them, like `09:30:00`, using `MID$` and `RIGHT$`. Run it, wait a minute, and run it again. Save it to a slot on the C64 page.

## Quiz

1. What does `? LEN("GAME ON")` show? (a) 6 (b) 7 (c) 2 (d) An error. **Answer: b**
2. What does `? LEFT$("FIREBALL",4)` show? (a) BALL (b) FIREB (c) FIRE (d) EBAL. **Answer: c**
3. What happens with `? "HP: "+20`? (a) HP: 20 (b) `?TYPE MISMATCH  ERROR` (c) HP: (d) 20. **Answer: b**
4. What is inside `STR$(5)`? (a) A space, then 5 (b) Just 5 (c) 05 (d) Nothing. **Answer: a**
5. What does `? VAL("42 GEMS")` show? (a) 0 (b) 42 GEMS (c) An error (d) 42. **Answer: d**
