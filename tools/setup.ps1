# One-time setup for the course site. Safe to run again: it skips what is
# already done. Run it through setup.bat (double-click).
#
#   1. Downloads portable PHP into runtime\php
#   2. Downloads the vc64web C64 emulator into runtime\vc64web (pinned version)
#   3. Copies the C64 ROMs from your VICE installation into runtime\roms
#
# Optional: setup.bat -ViceDir "D:\path\to\GTK3VICE-3.9-win64"

param([string]$ViceDir = '')

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'      # makes downloads much faster
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
Add-Type -AssemblyName System.IO.Compression.FileSystem

$Root    = Split-Path -Parent $PSScriptRoot
$Runtime = Join-Path $Root 'runtime'
New-Item -ItemType Directory -Force -Path $Runtime | Out-Null

$PhpUrl     = 'https://www.php.net/~windows/releases/latest/php-8.4-nts-Win32-vs17-x64-latest.zip'
$EmuCommit  = '469b63818d1a8f4d654fd3985b82aeb4e03fabba'
$EmuUrl     = "https://github.com/vc64web/vc64web.github.io/archive/$EmuCommit.zip"
$RomMirror  = 'https://raw.githubusercontent.com/VICE-Team/svn-mirror/main/vice/data'

function Step($text) { Write-Host ''; Write-Host "== $text" -ForegroundColor Cyan }
function Fail($text) { Write-Host ''; Write-Host $text -ForegroundColor Red; exit 1 }

# Unpack a zip, dropping its top folder and skipping paths that start
# with any of $Skip (relative to that top folder).
function Expand-Zip($Zip, $Dest, [string[]]$Skip = @()) {
    $archive = [IO.Compression.ZipFile]::OpenRead($Zip)
    try {
        foreach ($entry in $archive.Entries) {
            $rel = ($entry.FullName -split '/', 2)[1]
            if (-not $rel -or $rel.EndsWith('/')) { continue }
            if ($Skip | Where-Object { $rel.StartsWith($_) }) { continue }
            $target = Join-Path $Dest ($rel -replace '/', '\')
            New-Item -ItemType Directory -Force -Path (Split-Path -Parent $target) | Out-Null
            [IO.Compression.ZipFileExtensions]::ExtractToFile($entry, $target, $true)
        }
    } finally { $archive.Dispose() }
}

# ---------------------------------------------------------------- 1. PHP
Step 'Portable PHP'
$PhpDir = Join-Path $Runtime 'php'
$PhpExe = Join-Path $PhpDir 'php.exe'
if (Test-Path $PhpExe) {
    Write-Host 'Already installed.'
} else {
    $zip = Join-Path $Runtime 'php-download.zip'
    Write-Host 'Downloading PHP 8.4 for Windows (about 35 MB)...'
    Invoke-WebRequest -Uri $PhpUrl -OutFile $zip -UseBasicParsing
    Expand-Archive -Path $zip -DestinationPath $PhpDir -Force
    Remove-Item $zip
}
$ini = Get-Content (Join-Path $PhpDir 'php.ini-production')
$ini = $ini -replace '^;\s*extension=pdo_sqlite', 'extension=pdo_sqlite' `
            -replace '^;\s*extension=sqlite3', 'extension=sqlite3'
Set-Content -Path (Join-Path $PhpDir 'php.ini') -Value $ini
$modules = & $PhpExe -c (Join-Path $PhpDir 'php.ini') -d "extension_dir=$(Join-Path $PhpDir 'ext')" -m 2>&1
if ($LASTEXITCODE -ne 0 -or -not ($modules -match 'pdo_sqlite')) {
    Fail ("PHP didn't start. It usually needs the Microsoft Visual C++ Redistributable.`n" +
          "Install it from https://aka.ms/vs/17/release/vc_redist.x64.exe, then run setup.bat again.")
}
Write-Host 'PHP works, with SQLite.'

# ---------------------------------------------------------- 2. Emulator
Step 'vc64web emulator'
$EmuDir = Join-Path $Runtime 'vc64web'
$Stamp  = Join-Path $EmuDir '.version'
if ((Test-Path $Stamp) -and ((Get-Content $Stamp -Raw).Trim() -eq $EmuCommit)) {
    Write-Host 'Already installed.'
} else {
    $zip = Join-Path $Runtime 'vc64web-download.zip'
    Write-Host 'Downloading vc64web (about 10 MB)...'
    Invoke-WebRequest -Uri $EmuUrl -OutFile $zip -UseBasicParsing
    if (Test-Path $EmuDir) { Remove-Item -Recurse -Force $EmuDir }
    # doc\ is the project's demo website: not needed, and its long paths trip Windows.
    Expand-Zip $zip $EmuDir @('doc/', 'sw.js', 'sw_template.js')
    Remove-Item $zip
    # Our local copy sends nothing to third-party analytics.
    $index = Join-Path $EmuDir 'index.html'
    $html  = [IO.File]::ReadAllText($index)
    $html  = [regex]::Replace($html, '<script src=https://cloud\.umami\.is/script\.js[^>]*></script>', '')
    [IO.File]::WriteAllText($index, $html)
    Set-Content -Path $Stamp -Value $EmuCommit
    Write-Host 'Installed.'
}

# --------------------------------------------------------------- 3. ROMs
Step 'C64 ROMs'
$RomDir = Join-Path $Runtime 'roms'
New-Item -ItemType Directory -Force -Path $RomDir | Out-Null

# Our name -> (file names VICE uses, newest first), size, VICE subfolder
$Roms = @(
    @{ Name = 'basic.rom';   Files = @('basic-901226-01.bin', 'basic');     Size = 8192;  Sub = 'C64' },
    @{ Name = 'kernal.rom';  Files = @('kernal-901227-03.bin', 'kernal');   Size = 8192;  Sub = 'C64' },
    @{ Name = 'chargen.rom'; Files = @('chargen-901225-01.bin', 'chargen'); Size = 4096;  Sub = 'C64' },
    @{ Name = 'dos1541.rom'; Files = @('dos1541-325302-01+901229-05.bin', 'dos1541'); Size = 16384; Sub = 'DRIVES' }
)

function Test-Rom($Path, $Rom) {
    if (-not (Test-Path $Path)) { return $false }
    $bytes = [IO.File]::ReadAllBytes($Path)
    if ($bytes.Length -ne $Rom.Size) { return $false }
    # The standard character ROM starts with the '@' glyph. (The Japanese one doesn't.)
    if ($Rom.Name -eq 'chargen.rom' -and -not ($bytes[0] -eq 0x3C -and $bytes[1] -eq 0x66)) { return $false }
    return $true
}

$missing = @($Roms | Where-Object { -not (Test-Rom (Join-Path $RomDir $_.Name) $_) })
if ($missing.Count -eq 0) {
    Write-Host 'Already in place.'
} else {
    # Look for a VICE installation: the folder given, else common places.
    $places = @()
    if ($ViceDir) { $places += $ViceDir }
    foreach ($base in @($env:ProgramFiles, ${env:ProgramFiles(x86)}, "$env:USERPROFILE\Downloads",
                        "$env:USERPROFILE\Desktop", "$env:USERPROFILE\Documents", $env:USERPROFILE, 'C:\')) {
        if ($base -and (Test-Path $base)) {
            $places += @(Get-ChildItem -Path $base -Directory -Filter '*vice*' -ErrorAction SilentlyContinue |
                         ForEach-Object { $_.FullName })
        }
    }
    $vice = $null
    foreach ($place in $places) {
        $hit = Get-ChildItem -Path $place -Recurse -Depth 3 -Filter 'kernal*' -File -ErrorAction SilentlyContinue |
               Where-Object { $_.Length -eq 8192 -and $_.Directory.Name -eq 'C64' } | Select-Object -First 1
        if ($hit) { $vice = $hit.Directory.Parent.FullName; break }
    }

    if ($vice) {
        Write-Host "Found VICE in $vice"
        foreach ($rom in $missing) {
            foreach ($file in $rom.Files) {
                $src = Join-Path (Join-Path $vice $rom.Sub) $file
                if (Test-Rom $src $rom) { Copy-Item $src (Join-Path $RomDir $rom.Name) -Force; break }
            }
        }
    } else {
        Write-Host "VICE wasn't found on this computer."
        $answer = Read-Host 'Download the ROMs from the VICE project''s official GitHub mirror instead? (Y/N)'
        if ($answer -match '^[Yy]') {
            foreach ($rom in $missing) {
                Invoke-WebRequest -Uri "$RomMirror/$($rom.Sub)/$($rom.Files[0])" `
                                  -OutFile (Join-Path $RomDir $rom.Name) -UseBasicParsing
            }
        }
    }

    $still = @($Roms | Where-Object { -not (Test-Rom (Join-Path $RomDir $_.Name) $_) })
    if ($still.Count -gt 0) {
        Fail ("These ROMs are still missing: $(($still | ForEach-Object { $_.Name }) -join ', ').`n" +
              "Install VICE, or run: setup.bat -ViceDir ""C:\path\to\your\VICE folder""")
    }
    Write-Host 'ROMs in place.'
}

Write-Host ''
Write-Host 'Setup finished. Double-click start.bat to open the course.' -ForegroundColor Green
