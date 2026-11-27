<?php
// The course API. Everything answers in JSON except /api/prg/ID (raw bytes)
// and /api/listing/ID (plain text).
//
//   POST /api/submit        {exercise, prg (base64), capture}  -> new version
//   GET  /api/versions?exercise=ID                             -> list of versions
//   GET  /api/prg/ID                                           -> the PRG file
//   GET  /api/listing/ID                                       -> the listing
//   GET  /api/exercises                                        -> exercise list

require_once __DIR__ . '/db.php';
require_once __DIR__ . '/detokenize.php';
require_once __DIR__ . '/who.php';

function json_out($data, int $status = 200): void {
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
}

function exercise_ids(string $root): array {
    $list = json_decode(file_get_contents("$root/site/exercises.json"), true) ?: [];
    return array_column($list, 'id');
}

function handle_api(string $route, string $root): void {
    try {
        $method = $_SERVER['REQUEST_METHOD'];
        $c = client();

        if ($route === 'login' && $method === 'POST') {
            $in = json_decode(file_get_contents('php://input'), true) ?: [];
            $name = trim(preg_replace('/\s+/', ' ', (string)($in['name'] ?? '')));
            if (!preg_match("/^[\\p{L}\\p{N} ._'-]{1,30}$/u", $name)) {
                json_out(['error' => 'Use up to 30 letters, numbers and spaces.'], 400); return;
            }
            $pdo = db($root);
            $pdo->prepare('INSERT OR IGNORE INTO users (name) VALUES (?)')->execute([$name]);
            $q = $pdo->prepare('SELECT name FROM users WHERE name = ?'); $q->execute([$name]);
            $name = $q->fetchColumn();   // same capitalisation as the first time it was used
            setcookie('c64user', $name, ['expires' => time() + 365 * 86400, 'path' => '/', 'samesite' => 'Lax']);
            $_COOKIE['c64user'] = $name;
            log_visit($pdo, 'sign in');
            json_out(['name' => $name]);
            return;
        }
        if ($route === 'logout' && $method === 'POST') {
            setcookie('c64user', '', ['expires' => time() - 3600, 'path' => '/']);
            json_out(['ok' => true]);
            return;
        }
        if ($route === 'me' && $method === 'GET') {
            json_out(['name' => current_user(), 'device' => $c['device']]);
            return;
        }
        if ($route === 'visits' && $method === 'GET') {
            json_out(db($root)->query('SELECT user, ip, device, page, created_at FROM visits ORDER BY id DESC LIMIT 60')->fetchAll());
            return;
        }
        // Everything that saves needs a name.
        if ($method === 'POST' && !$c['user']) { json_out(['error' => 'Please sign in first.'], 401); return; }

        if ($route === 'exercises' && $method === 'GET') {
            header('Content-Type: application/json; charset=utf-8');
            readfile("$root/site/exercises.json");
            return;
        }

        if ($route === 'submit' && $method === 'POST') {
            $in = json_decode(file_get_contents('php://input'), true) ?: [];
            $exercise = (string)($in['exercise'] ?? '');
            if (!in_array($exercise, exercise_ids($root), true)) {
                json_out(['error' => 'Unknown exercise'], 400); return;
            }
            $prg = base64_decode((string)($in['prg'] ?? ''), true);
            if ($prg === false || strlen($prg) < 4 || strlen($prg) > 65536) {
                json_out(['error' => 'That doesn’t look like a C64 program'], 400); return;
            }
            $d = detokenize($prg);
            if ($d['lines'] === 0) {
                json_out(['error' => 'There’s no program in memory yet. Type a line with a line number first.'], 400); return;
            }
            $capture = in_array($in['capture'] ?? '', ['memory', 'upload'], true) ? $in['capture'] : 'memory';
            $pdo = db($root);
            $pdo->beginTransaction();
            $q = $pdo->prepare('SELECT COALESCE(MAX(version), 0) + 1 FROM submissions WHERE user = ? AND exercise = ?');
            $q->execute([$c['user'], $exercise]);
            $version = (int)$q->fetchColumn();
            $ins = $pdo->prepare('INSERT INTO submissions (exercise, version, prg, listing, capture, user, ip, device) VALUES (?, ?, ?, ?, ?, ?, ?, ?)');
            $ins->bindValue(1, $exercise);
            $ins->bindValue(2, $version, PDO::PARAM_INT);
            $ins->bindValue(3, $prg, PDO::PARAM_LOB);
            $ins->bindValue(4, $d['listing']);
            $ins->bindValue(5, $capture);
            $ins->bindValue(6, $c['user']);
            $ins->bindValue(7, $c['ip']);
            $ins->bindValue(8, $c['device']);
            $ins->execute();
            $id = (int)$pdo->lastInsertId();
            $pdo->commit();
            json_out(['id' => $id, 'version' => $version, 'lines' => $d['lines'],
                      'listing' => $d['listing'], 'warning' => $d['error']]);
            return;
        }

        if ($route === 'versions' && $method === 'GET') {
            $q = db($root)->prepare('SELECT id, version, created_at, listing FROM submissions WHERE user = ? AND exercise = ? ORDER BY version DESC');
            $q->execute([$c['user'], (string)($_GET['exercise'] ?? '')]);
            $rows = array_map(fn($r) => [
                'id' => (int)$r['id'], 'version' => (int)$r['version'], 'created_at' => $r['created_at'],
                'lines' => $r['listing'] === '' ? 0 : substr_count($r['listing'], "\n") + 1,
                'first' => strtok($r['listing'], "\n") ?: '',   // first line, so the workbook can show what was saved
            ], $q->fetchAll());
            json_out($rows);
            return;
        }

        if (preg_match('#^(prg|listing)/(\d+)$#', $route, $m) && $method === 'GET') {
            $q = db($root)->prepare('SELECT exercise, version, prg, listing FROM submissions WHERE id = ?');
            $q->execute([(int)$m[2]]);
            $row = $q->fetch();
            if (!$row) { json_out(['error' => 'No such version'], 404); return; }
            header('Cache-Control: no-store');
            if ($m[1] === 'prg') {
                header('Content-Type: application/octet-stream');
                header('Content-Disposition: attachment; filename="' . $row['exercise'] . '-v' . $row['version'] . '.prg"');
                echo $row['prg'];
            } else {
                header('Content-Type: text/plain; charset=utf-8');
                echo $row['listing'], "\n";
            }
            return;
        }

        // ---- Chapter work: content, quizzes, written responses ----
        $content = fn() => json_decode(file_get_contents("$root/site/content.json"), true) ?: [];

        if ($route === 'chapters' && $method === 'GET') {
            // Everything the page needs, minus the quiz answers.
            $out = array_map(function ($ch) {
                $ch['quiz'] = array_map(fn($q) => ['n' => $q['n'], 'question' => $q['question'], 'options' => $q['options']], $ch['quiz']);
                return $ch;
            }, $content());
            json_out($out);
            return;
        }

        if ($route === 'quiz' && $method === 'POST') {
            $in = json_decode(file_get_contents('php://input'), true) ?: [];
            $n = (int)($in['chapter'] ?? -1);
            $chapter = null;
            foreach ($content() as $one) if ($one['n'] === $n) $chapter = $one;   // not $c: that's who is signed in
            if (!$chapter || !$chapter['quiz']) { json_out(['error' => 'No quiz for that chapter'], 400); return; }
            $answers = $in['answers'] ?? [];
            $results = []; $score = 0;
            foreach ($chapter['quiz'] as $q) {
                $choice = strtolower((string)($answers[(string)$q['n']] ?? ''));
                $ok = $choice !== '' && $choice === $q['answer'];
                if ($ok) $score++;
                $results[] = ['n' => $q['n'], 'choice' => $choice, 'correct' => $ok];   // never the right letter: a retake means rethinking
            }
            $pdo = db($root);
            $pdo->beginTransaction();
            $pdo->prepare('INSERT INTO quiz_attempts (chapter, score, total, user, ip, device) VALUES (?, ?, ?, ?, ?, ?)')
                ->execute([$n, $score, count($results), $c['user'], $c['ip'], $c['device']]);
            $id = (int)$pdo->lastInsertId();
            $ins = $pdo->prepare('INSERT INTO quiz_answers (attempt_id, question, choice, correct) VALUES (?, ?, ?, ?)');
            foreach ($results as $r) $ins->execute([$id, $r['n'], $r['choice'], $r['correct'] ? 1 : 0]);
            $pdo->commit();
            json_out(['score' => $score, 'total' => count($results), 'results' => $results]);
            return;
        }

        if ($route === 'quiz-history' && $method === 'GET') {
            // Your own attempts, or everyone's with ?everyone=1 (the Editor's view).
            $q = db($root)->prepare('SELECT id, chapter, score, total, user, ip, device, created_at FROM quiz_attempts
                                     WHERE (? < 0 OR chapter = ?) AND (? = 1 OR user = ?) ORDER BY id DESC');
            $ch = isset($_GET['chapter']) ? (int)$_GET['chapter'] : -1;
            $q->bindValue(1, $ch, PDO::PARAM_INT); $q->bindValue(2, $ch, PDO::PARAM_INT);
            $q->bindValue(3, isset($_GET['everyone']) ? 1 : 0, PDO::PARAM_INT); $q->bindValue(4, $c['user']);
            $q->execute();
            json_out($q->fetchAll());
            return;
        }

        if ($route === 'response' && $method === 'POST') {
            $in = json_decode(file_get_contents('php://input'), true) ?: [];
            $kind = (string)($in['kind'] ?? '');
            $item = (string)($in['item'] ?? '');
            $text = trim((string)($in['text'] ?? ''));
            if (!in_array($kind, ['exercise', 'note'], true) || !preg_match('/^[\w.:-]{1,40}$/', $item) || strlen($text) > 20000) {
                json_out(['error' => 'That couldn’t be saved'], 400); return;
            }
            db($root)->prepare('INSERT INTO responses (chapter, kind, item, text, user, ip, device) VALUES (?, ?, ?, ?, ?, ?, ?)')
                     ->execute([(int)($in['chapter'] ?? 0), $kind, $item, $text, $c['user'], $c['ip'], $c['device']]);
            json_out(['saved' => true]);
            return;
        }

        if ($route === 'responses' && $method === 'GET') {
            // Newest version of each item, or the full history with ?all=1.
            $ch = isset($_GET['chapter']) ? (int)$_GET['chapter'] : -1;
            // Newest version of each item: your own, or everyone's with ?everyone=1.
            $sql = 'SELECT r.* FROM responses r JOIN (SELECT MAX(id) id FROM responses
                      WHERE (? < 0 OR chapter = ?) AND (? = 1 OR user = ?) GROUP BY user, chapter, kind, item) m
                    ON r.id = m.id ORDER BY r.user, r.chapter, r.kind, r.item';
            $q = db($root)->prepare($sql);
            $q->bindValue(1, $ch, PDO::PARAM_INT); $q->bindValue(2, $ch, PDO::PARAM_INT);
            $q->bindValue(3, isset($_GET['everyone']) ? 1 : 0, PDO::PARAM_INT); $q->bindValue(4, $c['user']);
            $q->execute();
            json_out($q->fetchAll());
            return;
        }

        if ($route === 'submissions' && $method === 'GET') {
            $q = db($root)->query('SELECT id, user, ip, device, exercise, version, listing, created_at FROM submissions ORDER BY id DESC LIMIT 50');
            json_out($q->fetchAll());
            return;
        }

        json_out(['error' => 'Unknown request'], 404);
    } catch (Throwable $e) {
        json_out(['error' => 'Server problem: ' . $e->getMessage()], 500);
    }
}
