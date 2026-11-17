<?php
// Turns a C64 BASIC program (PRG bytes) into a readable listing,
// the way LIST shows it. Control codes inside quotes are written in
// braces, like {clr} or {red}, the same style VICE's petcat uses.

const BASIC_TOKENS = [
    0x80 => 'END', 'FOR', 'NEXT', 'DATA', 'INPUT#', 'INPUT', 'DIM', 'READ',
    'LET', 'GOTO', 'RUN', 'IF', 'RESTORE', 'GOSUB', 'RETURN', 'REM',
    'STOP', 'ON', 'WAIT', 'LOAD', 'SAVE', 'VERIFY', 'DEF', 'POKE',
    'PRINT#', 'PRINT', 'CONT', 'LIST', 'CLR', 'CMD', 'SYS', 'OPEN',
    'CLOSE', 'GET', 'NEW', 'TAB(', 'TO', 'FN', 'SPC(', 'THEN',
    'NOT', 'STEP', '+', '-', '*', '/', '^', 'AND',
    'OR', '>', '=', '<', 'SGN', 'INT', 'ABS', 'USR',
    'FRE', 'POS', 'SQR', 'RND', 'LOG', 'EXP', 'COS', 'SIN',
    'TAN', 'ATN', 'PEEK', 'LEN', 'STR$', 'VAL', 'ASC', 'CHR$',
    'LEFT$', 'RIGHT$', 'MID$', 'GO',
    0xFF => '{pi}',
];

const PETSCII_CODES = [
    5 => 'wht', 13 => 'cr', 14 => 'lower', 17 => 'down', 18 => 'rvon', 19 => 'home',
    20 => 'del', 28 => 'red', 29 => 'rght', 30 => 'grn', 31 => 'blu',
    129 => 'orng', 133 => 'f1', 134 => 'f3', 135 => 'f5', 136 => 'f7',
    137 => 'f2', 138 => 'f4', 139 => 'f6', 140 => 'f8', 141 => 'sret',
    142 => 'upper', 144 => 'blk', 145 => 'up', 146 => 'rvof', 147 => 'clr',
    148 => 'inst', 149 => 'brn', 150 => 'lred', 151 => 'gry1', 152 => 'gry2',
    153 => 'lgrn', 154 => 'lblu', 155 => 'gry3', 156 => 'pur', 157 => 'left',
    158 => 'yel', 159 => 'cyn',
];

// One PETSCII byte as readable text (upper-case/graphics character set).
function petscii_char(int $b): string {
    if ($b === 0x5C) return '£';
    if ($b === 0x5E) return '^';      // up-arrow key
    if ($b === 0x5F) return '{left arrow}';
    if ($b >= 0x20 && $b <= 0x5D) return chr($b);
    if (isset(PETSCII_CODES[$b])) return '{' . PETSCII_CODES[$b] . '}';
    return sprintf('{$%02x}', $b);    // graphics and anything else
}

// Returns ['listing' => string, 'lines' => int, 'error' => ?string].
function detokenize(string $prg): array {
    $n = strlen($prg);
    if ($n < 4) return ['listing' => '', 'lines' => 0, 'error' => 'Too short to be a program'];
    $load = ord($prg[0]) | (ord($prg[1]) << 8);
    $mem = substr($prg, 2);
    $out = [];
    $pos = 0;
    for ($guard = 0; $guard < 10000; $guard++) {
        if ($pos + 4 > strlen($mem)) break;
        $next = ord($mem[$pos]) | (ord($mem[$pos + 1]) << 8);
        if ($next === 0) break;                       // end of program
        $lineNo = ord($mem[$pos + 2]) | (ord($mem[$pos + 3]) << 8);
        $i = $pos + 4;
        $text = '';
        $quoted = false;
        while ($i < strlen($mem) && ($b = ord($mem[$i])) !== 0) {
            if ($b === 0x22) { $quoted = !$quoted; $text .= '"'; }
            elseif (!$quoted && isset(BASIC_TOKENS[$b])) $text .= BASIC_TOKENS[$b];
            else $text .= petscii_char($b);
            $i++;
        }
        $out[] = "$lineNo $text";
        $newPos = $next - $load;
        if ($newPos <= $pos) {                        // broken link: stop safely
            return ['listing' => implode("\n", $out), 'lines' => count($out),
                    'error' => "Line links stop making sense after line $lineNo"];
        }
        $pos = $newPos;
    }
    return ['listing' => implode("\n", $out), 'lines' => count($out), 'error' => null];
}
