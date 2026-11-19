# One-time setup for the course site. Safe to run again: it skips what is
# already done. Run it through setup.bat (double-click).
#
#   0. Installs the Microsoft Visual C++ runtime if missing (PHP needs it)
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
$VcUrl      = 'https://aka.ms/vs/17/release/vc_redist.x64.exe'

function Step($text) { Write-Host ''; Write-Host "== $text" -ForegroundColor Cyan }
function Fail($text) { Write-Host ''; Write-Host $text -ForegroundColor Red; exit 1 }

# Download with retries, using the system proxy (and its sign-in) like a browser would.
# If a file of that name was already saved into runtime\ by hand, use it instead.
# If every attempt fails, explain how to download it in a browser instead.
# A zip that was cut off mid-download can't be opened; check before trusting one.
function Test-Zip($Path) {
    try { [IO.Compression.ZipFile]::OpenRead($Path).Dispose(); return $true } catch { return $false }
}

function Get-Download($Url, $Out, $What, $BrowserName = '') {
    $isZip = $Out.EndsWith('.zip')
    # 1. A saved copy that is incomplete (a cut-off zip) is thrown away.
    if ((Test-Path $Out) -and $isZip -and -not (Test-Zip $Out)) {
        Write-Host "The saved copy of $What is incomplete; setting it aside." -ForegroundColor Yellow
        Remove-Item $Out
    }
    # 2. A browser saves the file under its own name; if a good one is in the same folder, use it.
    if ($BrowserName -and -not (Test-Path $Out)) {
        $found = Get-ChildItem -Path (Split-Path $Out) -Filter $BrowserName -File -ErrorAction SilentlyContinue |
                 Where-Object { -not $isZip -or (Test-Zip $_.FullName) } | Select-Object -First 1
        if ($found) { Move-Item $found.FullName $Out; Write-Host "Found $What saved by a browser: $($found.Name)" }
    }
    # 3. A good saved copy is used as it is.
    if ((Test-Path $Out) -and ((Get-Item $Out).Length -gt 0)) {
        Write-Host "Using $What, already saved at $Out"
        return
    }
    $agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) thinking-in-c64-basic-setup'
    for ($try = 1; $try -le 3; $try++) {
        try {
            $proxy = [Net.WebRequest]::GetSystemWebProxy()
            $proxy.Credentials = [Net.CredentialCache]::DefaultCredentials
            [Net.WebRequest]::DefaultWebProxy = $proxy
            Invoke-WebRequest -Uri $Url -OutFile $Out -UseBasicParsing -UserAgent $agent
            if ((Test-Path $Out) -and ((Get-Item $Out).Length -gt 0) -and (-not $isZip -or (Test-Zip $Out))) { return }
            throw 'the download arrived incomplete'
        } catch {
            Write-Host "  Attempt $try didn't finish: $($_.Exception.Message)" -ForegroundColor Yellow
            Remove-Item $Out -ErrorAction SilentlyContinue
            Start-Sleep -Seconds (3 * $try)
        }
    }
    Fail ("Couldn't download $What. This often happens on work networks that filter downloads.`n" +
          "Instead, open this link in your browser:`n  $Url`n" +
          "save the file as:`n  $Out`n" +
          "then run setup.bat again. It will use the saved file.")
}

# ------------------------------------------- 0. Visual C++ runtime
Step 'Microsoft Visual C++ runtime (PHP needs it)'

# PHP 8.4's Windows build needs the runtime DLL at version 14.44 or later. Check the
# actual DLL, not the installer's registry record: the two can disagree.
$VcMin = [version]'14.44'
function Get-VCRuntimeVersion {
    $dll = Join-Path $env:SystemRoot 'System32\vcruntime140.dll'
    if (-not (Test-Path $dll)) { return $null }
    $fv = (Get-Item $dll).VersionInfo
    return [version]('{0}.{1}' -f $fv.FileMajorPart, $fv.FileMinorPart)
}
# When the DLL is in use, the installer queues the new one for the next restart.
function Test-VCRestartPending {
    $pending = (Get-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager' `
                -ErrorAction SilentlyContinue).PendingFileRenameOperations
    return [bool]($pending | Where-Object { $_ -match 'vcruntime140' })
}
$RestartMsg = ("A newer Visual C++ runtime is installed, but Windows will only switch to it after a restart`n" +
               "(the old one was in use). Restart the computer, then run setup.bat again.")

$found = Get-VCRuntimeVersion
if ($found -and $found -ge $VcMin) {
    Write-Host "Already installed (version $found)."
} else {
    if ($found) { Write-Host "Found version $found, but PHP needs $VcMin or later." }
    else        { Write-Host 'Not installed.' }
    if (Test-VCRestartPending) { Fail $RestartMsg }
    $vc = Join-Path $Runtime 'vc_redist.x64.exe'
    Write-Host 'Downloading Microsoft''s installer (about 25 MB)...'
    Get-Download $VcUrl $vc 'the Visual C++ installer'
    Write-Host 'Installing. Windows will ask for permission, because it installs for the whole computer.'
    try {
        $proc = Start-Process -FilePath $vc -ArgumentList '/install', '/passive', '/norestart' -Verb RunAs -Wait -PassThru
    } catch {
        Fail "The Visual C++ installer didn't run (the permission prompt may have been declined). Run setup.bat again to retry."
    } finally {
        Remove-Item $vc -ErrorAction SilentlyContinue
    }
    # 3010 = installed, restart required
    if ($proc.ExitCode -eq 3010 -or ((Get-VCRuntimeVersion) -lt $VcMin -and (Test-VCRestartPending))) { Fail $RestartMsg }
    $found = Get-VCRuntimeVersion
    if (-not ($found -and $found -ge $VcMin)) {
        Fail ("The Visual C++ runtime is still too old or missing. Install it by hand from`n$VcUrl`n" +
              "then run setup.bat again.")
    }
    Write-Host "Installed (version $found)."
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
    Get-Download $PhpUrl $zip 'PHP' 'php-*-Win32-*.zip'
    Expand-Archive -Path $zip -DestinationPath $PhpDir -Force
    Remove-Item $zip
}
$ini = Get-Content (Join-Path $PhpDir 'php.ini-production')
$ini = $ini -replace '^;\s*extension=pdo_sqlite', 'extension=pdo_sqlite' `
            -replace '^;\s*extension=sqlite3', 'extension=sqlite3'
Set-Content -Path (Join-Path $PhpDir 'php.ini') -Value $ini
# PHP prints warnings on stderr; don't let PowerShell treat them as fatal here.
$ErrorActionPreference = 'Continue'
$modules = (& $PhpExe -c (Join-Path $PhpDir 'php.ini') -d "extension_dir=$(Join-Path $PhpDir 'ext')" -m 2>&1 | Out-String)
$phpExit = $LASTEXITCODE
$ErrorActionPreference = 'Stop'
if ($phpExit -ne 0 -or $modules -notmatch 'pdo_sqlite' -or $modules -match 'Warning') {
    Write-Host $modules
    Fail ("PHP didn't start, even though the Visual C++ runtime is installed.`n" +
          "Paste the lines above into the chat so we can see why.")
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
    Get-Download $EmuUrl $zip 'the vc64web emulator' '*469b63818d1a8f4d654fd3985b82aeb4e03fabba*.zip'
    if (Test-Path $EmuDir) { Remove-Item -Recurse -Force $EmuDir }
    # Unpack with Windows' own tar.exe (it reads zip files). Called by full path, because
    # PortableGit ships a different tar that can't. Drop the archive's top folder; skip
    # doc\ (the project's demo website: not needed, and its long paths trip Windows) and
    # the offline-cache service worker.
    New-Item -ItemType Directory -Force -Path $EmuDir | Out-Null
    & (Join-Path $env:SystemRoot 'System32\tar.exe') -xf $zip -C $EmuDir --strip-components 1 `
        --exclude '*/doc/*' --exclude '*/sw.js' --exclude '*/sw_template.js'
    if ($LASTEXITCODE -ne 0) { Fail "Unpacking vc64web failed (tar exit code $LASTEXITCODE)." }
    Remove-Item $zip
    foreach ($needed in @('index.html', 'vc64.js', 'vc64.wasm')) {
        if (-not (Test-Path (Join-Path $EmuDir $needed))) { Fail "Unpacking vc64web left out $needed. Paste this window into the chat." }
    }
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
                Get-Download "$RomMirror/$($rom.Sub)/$($rom.Files[0])" (Join-Path $RomDir $rom.Name) "the ROM file $($rom.Name)"
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
