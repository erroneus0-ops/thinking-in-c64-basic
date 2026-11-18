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
        user        TEXT    NOT NULL DEFAULT \'\',
        ip          TEXT    NOT NULL DEFAULT \'\',
        device      TEXT    NOT NULL DEFAULT \'\',
        exercise    TEXT    NOT NULL,
        version     INTEGER NOT NULL,
        prg         BLOB    NOT NULL,
        listing     TEXT    NOT NULL,
        capture     TEXT    NOT NULL,
        created_at  TEXT    NOT NULL DEFAULT (datetime(\'now\', \'localtime\')),
        UNIQUE (user, exercise, version)
    )');
    $pdo->exec('CREATE TABLE IF NOT EXISTS quiz_attempts (
        id          INTEGER PRIMARY KEY,
        chapter     INTEGER NOT NULL,
        score       INTEGER NOT NULL,
        total       INTEGER NOT NULL,
        created_at  TEXT    NOT NULL DEFAULT (datetime(\'now\', \'localtime\'))
    )');
    $pdo->exec('CREATE TABLE IF NOT EXISTS quiz_answers (
        attempt_id  INTEGER NOT NULL REFERENCES quiz_attempts(id),
        question    INTEGER NOT NULL,
        choice      TEXT    NOT NULL,
        correct     INTEGER NOT NULL
    )');
    // Written work: exercise answers and beta tester notes. Every save is a new row,
    // so nothing is ever overwritten; the newest row per item is the current one.
    $pdo->exec('CREATE TABLE IF NOT EXISTS responses (
        id          INTEGER PRIMARY KEY,
        chapter     INTEGER NOT NULL,
        kind        TEXT    NOT NULL,   -- exercise | note
        item        TEXT    NOT NULL,   -- e.g. ex2, or 1.3:boring
        text        TEXT    NOT NULL,
        created_at  TEXT    NOT NULL DEFAULT (datetime(\'now\', \'localtime\'))
    )');
    $pdo->exec('CREATE TABLE IF NOT EXISTS users (
        id          INTEGER PRIMARY KEY,
        name        TEXT    NOT NULL UNIQUE COLLATE NOCASE,
        created_at  TEXT    NOT NULL DEFAULT (datetime(\'now\', \'localtime\'))
    )');
    $pdo->exec('CREATE TABLE IF NOT EXISTS visits (
        id          INTEGER PRIMARY KEY,
        user        TEXT    NOT NULL,
        ip          TEXT    NOT NULL,
        device      TEXT    NOT NULL,
        agent       TEXT    NOT NULL,
        page        TEXT    NOT NULL,
        created_at  TEXT    NOT NULL DEFAULT (datetime(\'now\', \'localtime\'))
    )');
    upgrade_tables($pdo);
    return $pdo;
}

function has_column(PDO $pdo, string $table, string $col): bool {
    foreach ($pdo->query("PRAGMA table_info($table)") as $r) if ($r['name'] === $col) return true;
    return false;
}

// Databases made before sign-in existed get the new columns. Earlier rows are kept and
// labelled "(before sign-in)". Submissions are rebuilt because version numbers become
// per person (the UNIQUE rule changes), which SQLite can only do by copying the table.
function upgrade_tables(PDO $pdo): void {
    $before = "'(before sign-in)'";
    foreach (['quiz_attempts', 'responses'] as $t) {
        if (!has_column($pdo, $t, 'user')) {
            $pdo->exec("ALTER TABLE $t ADD COLUMN user TEXT NOT NULL DEFAULT $before");
            $pdo->exec("ALTER TABLE $t ADD COLUMN ip TEXT NOT NULL DEFAULT ''");
            $pdo->exec("ALTER TABLE $t ADD COLUMN device TEXT NOT NULL DEFAULT ''");
        }
    }
    if (!has_column($pdo, 'submissions', 'user')) {
        $pdo->beginTransaction();
        $pdo->exec('ALTER TABLE submissions RENAME TO submissions_old');
        $pdo->exec("CREATE TABLE submissions (
            id INTEGER PRIMARY KEY, user TEXT NOT NULL DEFAULT '', ip TEXT NOT NULL DEFAULT '',
            device TEXT NOT NULL DEFAULT '', exercise TEXT NOT NULL, version INTEGER NOT NULL,
            prg BLOB NOT NULL, listing TEXT NOT NULL, capture TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
            UNIQUE (user, exercise, version))");
        $pdo->exec("INSERT INTO submissions (id, user, exercise, version, prg, listing, capture, created_at)
                    SELECT id, $before, exercise, version, prg, listing, capture, created_at FROM submissions_old");
        $pdo->exec('DROP TABLE submissions_old');
        $pdo->commit();
    }
}
