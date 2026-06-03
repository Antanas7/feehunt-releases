@echo off
setlocal
cd /d "%~dp0dist_rebuilt\FeeHunt"
start "" "%CD%\FeeHunt.exe"
exit /b
