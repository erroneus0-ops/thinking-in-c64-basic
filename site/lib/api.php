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
            $q = $pdo->prepare('SELECT COALESCE(MAX(version), 0) + 1 FROM submissions WHERE exercise = ?');
            $q->execute([$exercise]);
            $version = (int)$q->fetchColumn();
            $ins = $pdo->prepare('INSERT INTO submissions (exercise, version, prg, listing, capture) VALUES (?, ?, ?, ?, ?)');
            $ins->bindValue(1, $exercise);
            $ins->bindValue(2, $version, PDO::PARAM_INT);
            $ins->bindValue(3, $prg, PDO::PARAM_LOB);
            $ins->bindValue(4, $d['listing']);
            $ins->bindValue(5, $capture);
            $ins->execute();
            $id = (int)$pdo->lastInsertId();
            $pdo->commit();
            json_out(['id' => $id, 'version' => $version, 'lines' => $d['lines'],
                      'listing' => $d['listing'], 'warning' => $d['error']]);
            return;
        }

        if ($route === 'versions' && $method === 'GET') {
            $q = db($root)->prepare('SELECT id, version, created_at, listing FROM submissions WHERE exercise = ? ORDER BY version DESC');
            $q->execute([(string)($_GET['exercise'] ?? '')]);
            $rows = array_map(fn($r) => [
                'id' => (int)$r['id'], 'version' => (int)$r['version'], 'created_at' => $r['created_at'],
                'lines' => $r['listing'] === '' ? 0 : substr_count($r['listing'], "\n") + 1,
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

        json_out(['error' => 'Unknown request'], 404);
    } catch (Throwable $e) {
        json_out(['error' => 'Server problem: ' . $e->getMessage()], 500);
    }
}
