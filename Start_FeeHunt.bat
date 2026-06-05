@echo off
setlocal
cd /d "%~dp0dist_current\FeeHunt"
start "" "%CD%\FeeHunt.exe"
exit /b
