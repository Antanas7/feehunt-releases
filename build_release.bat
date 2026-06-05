@echo off
setlocal enabledelayedexpansion

REM ============================================================
REM  FeeHunt universal release builder
REM  Usage:  build_release.bat 1.12.5
REM          build_release.bat 1.12.6
REM
REM  Steps:
REM    1. Set APP_VERSION in config.py
REM    2. Clean old build\ and dist\FeeHunt
REM    3. PyInstaller rebuild  -> dist\FeeHunt
REM    4. Copy to dist_v<compact>\FeeHunt  (e.g. dist_v1125)
REM    5. Inno Setup compile -> dist_installer\FeeHunt-Setup-v<ver>.exe
REM
REM  NOTE: produced .exe is UNSIGNED. Microsoft Store requires a
REM        code-signing certificate (Policy 10.2.9). Unsigned build
REM        is fine for feehunt.pro/download distribution.
REM ============================================================

if "%~1"=="" (
  echo ERROR: missing version argument.
  echo Usage: build_release.bat 1.12.5
  exit /b 1
)

set "VERSION=%~1"
set "COMPACT=%VERSION:.=%"
set "SRCDIR=dist_v%COMPACT%\FeeHunt"
REM Inno Setup ISCC.exe: try common install locations (per-user and machine-wide)
set "ISCC=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist "%ISCC%" set "ISCC=%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe"
if not exist "%ISCC%" set "ISCC=C:\Program Files\Inno Setup 6\ISCC.exe"

echo.
echo === FeeHunt release build v%VERSION% ===
echo     source folder : %SRCDIR%
echo     installer out : dist_installer\FeeHunt-Setup-v%VERSION%.exe
echo.

REM --- 1. Update APP_VERSION in config.py (UTF-8, no BOM) ---
echo [1/5] Setting APP_VERSION = "%VERSION%" in config.py
set "FH_VER=%VERSION%"
powershell -NoProfile -Command "$p=(Resolve-Path 'config.py').Path; $c=[System.IO.File]::ReadAllText($p); $c=[regex]::Replace($c,'APP_VERSION = \"[^\"]*\"','APP_VERSION = \"'+$env:FH_VER+'\"'); [System.IO.File]::WriteAllText($p,$c,(New-Object System.Text.UTF8Encoding $false))"
if errorlevel 1 ( echo ERROR: failed to update config.py & exit /b 1 )

REM Verify the value actually landed
powershell -NoProfile -Command "if (-not ((Get-Content 'config.py') -match 'APP_VERSION = \"%VERSION%\"')) { exit 1 }"
if errorlevel 1 ( echo ERROR: APP_VERSION not set to %VERSION% in config.py & exit /b 1 )

REM --- 2. Clean previous build output ---
echo [2/5] Cleaning build\FeeHunt and dist\FeeHunt
if exist "build\FeeHunt" rmdir /s /q "build\FeeHunt"
if exist "dist\FeeHunt" rmdir /s /q "dist\FeeHunt"

REM --- 3. PyInstaller rebuild ---
REM Prefer the project virtualenv; fall back to PATH.
set "PYINSTALLER=pyinstaller"
if exist ".venv\Scripts\pyinstaller.exe" set "PYINSTALLER=.venv\Scripts\pyinstaller.exe"
echo [3/5] Running PyInstaller via "%PYINSTALLER%" (this can take a few minutes)...
"%PYINSTALLER%" FeeHunt.spec --noconfirm
if errorlevel 1 ( echo ERROR: PyInstaller failed & exit /b 1 )
if not exist "dist\FeeHunt\FeeHunt.exe" ( echo ERROR: dist\FeeHunt\FeeHunt.exe not found after build & exit /b 1 )

REM --- 4. Copy to versioned source folder ---
echo [4/5] Copying dist\FeeHunt -> %SRCDIR%
if exist "dist_v%COMPACT%" rmdir /s /q "dist_v%COMPACT%"
xcopy /e /i /q /y "dist\FeeHunt" "%SRCDIR%" >nul
if errorlevel 1 ( echo ERROR: copy to %SRCDIR% failed & exit /b 1 )

REM --- 5. Inno Setup compile ---
echo [5/5] Compiling installer with Inno Setup...
if not exist "%ISCC%" ( echo ERROR: ISCC.exe not found at "%ISCC%" & exit /b 1 )
"%ISCC%" /DMyAppVersion=%VERSION% "/DSourceDir=%SRCDIR%" FeeHuntSetup.iss
if errorlevel 1 ( echo ERROR: Inno Setup compile failed & exit /b 1 )

echo.
echo === DONE ===
echo Installer: dist_installer\FeeHunt-Setup-v%VERSION%.exe
echo.
echo REMINDER: this .exe is UNSIGNED. Sign it before Microsoft Store submission.
echo           signtool sign /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 /a dist_installer\FeeHunt-Setup-v%VERSION%.exe
echo.
endlocal
