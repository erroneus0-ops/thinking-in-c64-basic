@echo off
rem One-time setup: downloads PHP and the C64 emulator, copies the C64 ROMs.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\setup.ps1" %*
echo.
echo Press Space or Enter to close this window.
pause >nul
