<?php
// Router for PHP's built-in web server. Started by start.bat:
//   php -S 0.0.0.0:8064 -t site site/router.php
// Decides what each web address serves. Files outside site/ (the book,
// the emulator, the ROMs) are served from their own folders.

$ROOT = dirname(__DIR__);
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
if (str_starts_with($path, '/book/')) { serve_from("$ROOT/docs", substr($path, 6)); return true; }
if (str_starts_with($path, '/assets/')) { serve_from(__DIR__ . '/assets', substr($path, 8)); return true; }

$pages = ['/' => 'index.html', '/c64' => 'c64.html'];
if (isset($pages[$path])) { serve_from(__DIR__ . '/pages', $pages[$path]); return true; }

http_response_code(404);
header('Content-Type: text/plain; charset=utf-8');
echo "Not found: $path\n";
return true;
