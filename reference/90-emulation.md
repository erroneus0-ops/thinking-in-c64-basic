# Emulation notes

This chapter collects facts about running BASIC V2 under emulation. It cannot be complete: emulators change and new ones appear. It records what has been verified, and where it came from, so that differences in other or later emulators can be recognized and worked out.

## The course site (vc64web)

The course site embeds vc64web, a browser build of the VirtualC64 emulator, pinned to a fixed version. vc64web maps no PC key to several C64 keys; the course site adds these mappings:

| C64 key | PC key on the course site |
| --- | --- |
| RUN/STOP | Esc |
| RESTORE | Page Up |
| CLR/HOME | Home (often Fn + Left Arrow on laptops) |
| SHIFT + CLR/HOME (clear screen) | Shift + Home |
| SHIFT + INST/DEL (insert) | Insert, or Shift + Backspace (vc64web otherwise ignores Shift on Backspace and deletes) |
| ↑ (power) | ^ (Shift + 6 on most layouts) |

Shift-click on the C64 screen moves the cursor by feeding cursor-key codes through the KERNAL keyboard buffer, only while BASIC is in direct mode, waiting for input, and not in quote or insert mode. This is a feature of the course site, not of the C64.

## ROM files

An emulated C64 requires copies of the original ROMs, which remain under copyright and are not distributed with the course site. The course site's setup copies them from a local VICE installation.

| File | Size | Contents |
| --- | --- | --- |
| `basic.rom` | 8192 bytes | BASIC V2 interpreter |
| `kernal.rom` | 8192 bytes | KERNAL operating system |
| `chargen.rom` | 4096 bytes | Character generator (the C64's font). The standard ROM (901225-01) begins with the bytes 3C 66 6E; a Japanese character ROM (906143-02) differs and must not be used. |
| `dos1541.rom` | 16384 bytes | 1541 disk drive firmware, required for disk images |

## To be collected

VICE keyboard mappings (positional and symbolic), disk image formats (.d64, .g64), tape images (.tap, .t64), cartridge images (.crt), and differences between emulators, each with its source.
