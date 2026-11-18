# A Maze in Two Lines

Before anything else, let's make the C64 do something worth seeing.

Click the C64 screen. Type these two lines exactly as shown, and press RETURN at the end of each one. Keep Caps Lock off: type ordinary small letters, and the C64 will show them as capitals.

```
10 PRINT CHR$(205.5 + RND(1));
20 GOTO 10
```

Now type this and press RETURN:

```
RUN
```

A maze fills the screen, row after row, and never stops. Run it again and you get a different maze. No two are ever the same.

To stop it, press **RUN/STOP**. On a PC keyboard, that's **Esc**. The C64 answers `BREAK IN 10` (or `20`) and `READY.`

Right now this probably looks like magic. It isn't. Every piece has a meaning, and this book teaches you each one:

| Piece | What it does | Taught in |
| --- | --- | --- |
| `10` and `20` | Line numbers: the order of the steps | Chapter 2 |
| `PRINT` | Puts something on the screen | Chapter 1 |
| `;` | Keeps the next thing on the same row | Chapter 1 |
| `RND(1)` | Picks a random number | Chapter 3 |
| `CHR$( )` | Turns a number into a character | Chapter 4 |
| `GOTO 10` | Jumps back to line 10 | Chapter 9 |

When you finish Chapter 9, come back to this page. You'll be able to explain every character in it.

::: good-to-know
Programmers sometimes squeeze this same maze into a single, very short line, as a kind of puzzle. It works, but it's hard to read. This book always writes programs to be read, because a program you can read is a program you can fix.
:::
