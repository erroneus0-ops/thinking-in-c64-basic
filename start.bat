@echo off
rem Starts the course site. Keep this window open while working; close it to stop.
rem Port: 8064 unless given, e.g. "start.bat 80" (a shortcut can pass it).
setlocal
cd /d "%~dp0"
set PORT=8064
if not "%~1"=="" set PORT=%~1
set SHOWPORT=:%PORT%
if "%PORT%"=="80" set SHOWPORT=

if not exist "runtime\php\php.exe" (
    echo The course isn't set up on this computer yet. Double-click setup.bat first.
    echo Press Space or Enter to close this window.
    pause >nul
    exit /b 1
)

set LANIP=
for /f "usebackq delims=" %%i in (`powershell -NoProfile -ExecutionPolicy Bypass -File "tools\lanip.ps1"`) do set LANIP=%%i

echo.
echo   Thinking in C64 BASIC is running.
echo.
echo   On this computer:             http://localhost%SHOWPORT%/
if defined LANIP echo   On a phone on the same Wi-Fi:  http://%LANIP%%SHOWPORT%/
echo.
echo   Keep this window open while you work. Close it to stop the course site.
echo.

start "" "http://localhost%SHOWPORT%/"
"runtime\php\php.exe" -c "runtime\php\php.ini" -d extension_dir="%~dp0runtime\php\ext" -S 0.0.0.0:%PORT% -t site site\router.php
