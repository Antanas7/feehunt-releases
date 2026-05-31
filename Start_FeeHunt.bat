@echo off
setlocal
cd /d "%~dp0dist\FeeHunt"
start "" "%CD%\FeeHunt.exe"
exit /b
