<?php
// Who is using the site, and from what. Sign-in is a name only (a family LAN site);
// every save and page visit also records the IP address and the kind of device.

function current_user(): ?string {
    $n = trim((string)($_COOKIE['c64user'] ?? ''));
    return preg_match("/^[\\p{L}\\p{N} ._'-]{1,30}$/u", $n) ? $n : null;
}

function client(): array {
    $ua = (string)($_SERVER['HTTP_USER_AGENT'] ?? '');
    $kind = preg_match('/iPad|Tablet|Android(?!.*Mobile)/i', $ua) ? 'Tablet'
          : (preg_match('/Mobi|iPhone|Android/i', $ua) ? 'Phone' : 'Computer');
    $os = preg_match('/Windows/i', $ua) ? 'Windows'
        : (preg_match('/Android/i', $ua) ? 'Android'
        : (preg_match('/iPhone|iPad|iOS/i', $ua) ? 'iOS'
        : (preg_match('/Macintosh|Mac OS X/i', $ua) ? 'Mac'
        : (preg_match('/Linux|X11|CrOS/i', $ua) ? 'Linux' : 'unknown'))));
    return ['user' => current_user() ?? '', 'ip' => (string)($_SERVER['REMOTE_ADDR'] ?? ''),
            'device' => "$kind ($os)", 'agent' => substr($ua, 0, 300)];
}

function log_visit(PDO $pdo, string $page): void {
    $c = client();
    $pdo->prepare('INSERT INTO visits (user, ip, device, agent, page) VALUES (?, ?, ?, ?, ?)')
        ->execute([$c['user'], $c['ip'], $c['device'], $c['agent'], $page]);
}
