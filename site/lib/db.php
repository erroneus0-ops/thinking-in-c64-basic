<?php
// The course database: one SQLite file in data/, created on first use.
// Student work is only ever added to, never overwritten.

function db(string $root): PDO {
    static $pdo = null;
    if ($pdo) return $pdo;
    $dir = "$root/data";
    if (!is_dir($dir)) mkdir($dir, 0775, true);
    $pdo = new PDO("sqlite:$dir/course.sqlite");
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
    $pdo->exec('PRAGMA journal_mode = WAL');
    $pdo->exec('CREATE TABLE IF NOT EXISTS submissions (
        id          INTEGER PRIMARY KEY,
        exercise    TEXT    NOT NULL,
        version     INTEGER NOT NULL,
        prg         BLOB    NOT NULL,
        listing     TEXT    NOT NULL,
        capture     TEXT    NOT NULL,
        created_at  TEXT    NOT NULL DEFAULT (datetime(\'now\', \'localtime\')),
        UNIQUE (exercise, version)
    )');
    return $pdo;
}
