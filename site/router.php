<?php
// Router for PHP's built-in web server. Started by start.bat:
//   php -S 0.0.0.0:8064 -t site site/router.php
// Decides what each web address serves. Files outside site/ (the book,
// the emulator, the ROMs) are served from their own folders.

$ROOT = dirname(__DIR__);

// Log every request to the start.bat window: who, what, result, size. PHP's server
// stops logging details once a router script handles the request, so we do it here.
$started = microtime(true);
register_shutdown_function(function () use ($started) {
    $status = http_response_code() ?: 200;
    $bytes = 0;
    foreach (headers_list() as $h) if (stripos($h, 'Content-Length:') === 0) $bytes = (int)trim(substr($h, 15));
    error_log(sprintf('%s %s %s -> %d (%s, %d ms)',
        $_SERVER['REMOTE_ADDR'] ?? '?', $_SERVER['REQUEST_METHOD'] ?? '?', $_SERVER['REQUEST_URI'] ?? '?',
        $status, $bytes ? number_format($bytes) . ' bytes' : 'no size', (microtime(true) - $started) * 1000));
});
$path = rawurldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH) ?? '/');

const MIME = [
    'html' => 'text/html; charset=utf-8', 'htm' => 'text/html; charset=utf-8',
    'js' => 'text/javascript; charset=utf-8', 'mjs' => 'text/javascript; charset=utf-8',
    'css' => 'text/css; charset=utf-8', 'json' => 'application/json',
    'wasm' => 'application/wasm', 'svg' => 'image/svg+xml', 'png' => 'image/png',
    'jpg' => 'image/jpeg', 'jpeg' => 'image/jpeg', 'gif' => 'image/gif',
    'ico' => 'image/x-icon', 'webp' => 'image/webp', 'pdf' => 'application/pdf',
    'woff' => 'font/woff', 'woff2' => 'font/woff2', 'ttf' => 'font/ttf',
    'mp3' => 'audio/mpeg', 'wav' => 'audio/wav', 'ogg' => 'audio/ogg',
    'txt' => 'text/plain; charset=utf-8', 'webmanifest' => 'application/manifest+json',
];

// Serve one file from inside $base, refusing anything that escapes it.
function serve_from(string $base, string $rel, bool $cache = false): void {
    $baseReal = realpath($base);
    $file = $baseReal ? realpath($baseReal . '/' . ltrim($rel, '/')) : false;
    if ($file && is_dir($file)) $file = realpath($file . '/index.html');
    if (!$file || !str_starts_with($file, $baseReal) || !is_file($file)) {
        http_response_code(404);
        header('Content-Type: text/plain; charset=utf-8');
        echo "Not found: $rel\n";
        return;
    }
    $ext = strtolower(pathinfo($file, PATHINFO_EXTENSION));
    header('Content-Type: ' . (MIME[$ext] ?? 'application/octet-stream'));
    header('Content-Length: ' . filesize($file));
    header($cache ? 'Cache-Control: public, max-age=86400' : 'Cache-Control: no-cache');
    readfile($file);
}

if (str_starts_with($path, '/api/')) {
    require __DIR__ . '/lib/api.php';
    handle_api(substr($path, 5), $ROOT);
    return true;
}
if (str_starts_with($path, '/emu/'))  { serve_from("$ROOT/runtime/vc64web", substr($path, 5), true); return true; }
if (str_starts_with($path, '/roms/')) { serve_from("$ROOT/runtime/roms", substr($path, 6), true); return true; }
if ($path === '/book')                { header('Location: /book/'); return true; }
if (str_starts_with($path, '/book/')) {
    if (preg_match('#^/book/(index\.html)?$#', $path)) {   // the book itself, not its images or PDF
        require_once __DIR__ . '/lib/db.php';
        require_once __DIR__ . '/lib/who.php';
        log_visit(db($ROOT), '/book');
    }
    serve_from("$ROOT/docs", substr($path, 6));
    return true;
}
if (str_starts_with($path, '/assets/')) { serve_from(__DIR__ . '/assets', substr($path, 8)); return true; }

$pages = ['/' => 'index.html', '/c64' => 'c64.html', '/work' => 'work.html', '/review' => 'review.html', '/login' => 'login.html'];
if (isset($pages[$path])) {
    // The C64 and Chapter work pages need a name; their visits are logged with IP and device.
    if (in_array($path, ['/c64', '/work'], true)) {
        require_once __DIR__ . '/lib/db.php';
        require_once __DIR__ . '/lib/who.php';
        if (!current_user()) { header('Location: /login?next=' . rawurlencode($path)); return true; }
        log_visit(db($ROOT), $path);
    }
    serve_from(__DIR__ . '/pages', $pages[$path]);
    return true;
}

http_response_code(404);
header('Content-Type: text/plain; charset=utf-8');
echo "Not found: $path\n";
return true;
