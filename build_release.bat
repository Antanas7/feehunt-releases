@echo off
setlocal enabledelayedexpansion

REM Always run from this script's own folder (relative paths below depend on it)
cd /d "%~dp0"

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
REM    5. Code-sign the inner app exe (FeeHunt.exe) before packaging
REM    6. Inno Setup compile -> dist_installer\FeeHunt-Setup-v<ver>.exe
REM    7. Code-sign the installer
REM
REM  Both signings use sign_installer.ps1 (config from signing.local.ps1 / env
REM  vars; SSL.com password + TOTP secret are prompted unless set in env). You
REM  will be prompted once per signed file. If CodeSignTool is not installed,
REM  signing is skipped and the unsigned files are kept (build still succeeds).
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
echo [1/7] Setting APP_VERSION = "%VERSION%" in config.py
set "FH_VER=%VERSION%"
powershell -NoProfile -Command "$p=(Resolve-Path 'config.py').Path; $c=[System.IO.File]::ReadAllText($p); $c=[regex]::Replace($c,'APP_VERSION = \"[^\"]*\"','APP_VERSION = \"'+$env:FH_VER+'\"'); [System.IO.File]::WriteAllText($p,$c,(New-Object System.Text.UTF8Encoding $false))"
if errorlevel 1 ( echo ERROR: failed to update config.py & exit /b 1 )

REM Verify the value actually landed
powershell -NoProfile -Command "if (-not ((Get-Content 'config.py') -match 'APP_VERSION = \"%VERSION%\"')) { exit 1 }"
if errorlevel 1 ( echo ERROR: APP_VERSION not set to %VERSION% in config.py & exit /b 1 )

REM --- 2. Clean previous build output ---
echo [2/7] Cleaning build\FeeHunt and dist\FeeHunt
if exist "build\FeeHunt" rmdir /s /q "build\FeeHunt"
if exist "dist\FeeHunt" rmdir /s /q "dist\FeeHunt"

REM --- 3. PyInstaller rebuild ---
REM Prefer the project virtualenv; fall back to PATH.
set "PYINSTALLER=pyinstaller"
if exist ".venv\Scripts\pyinstaller.exe" set "PYINSTALLER=.venv\Scripts\pyinstaller.exe"
echo [3/7] Running PyInstaller via "%PYINSTALLER%" (this can take a few minutes)...
"%PYINSTALLER%" FeeHunt.spec --noconfirm
if errorlevel 1 ( echo ERROR: PyInstaller failed & exit /b 1 )
if not exist "dist\FeeHunt\FeeHunt.exe" ( echo ERROR: dist\FeeHunt\FeeHunt.exe not found after build & exit /b 1 )

REM --- 4. Copy to versioned source folder ---
echo [4/7] Copying dist\FeeHunt -> %SRCDIR%
if exist "dist_v%COMPACT%" rmdir /s /q "dist_v%COMPACT%"
xcopy /e /i /q /y "dist\FeeHunt" "%SRCDIR%" >nul
if errorlevel 1 ( echo ERROR: copy to %SRCDIR% failed & exit /b 1 )

REM --- 5. Code-sign the inner app exe BEFORE Inno Setup packages it ---
echo [5/7] Signing inner app exe (%SRCDIR%\FeeHunt.exe)...
powershell -NoProfile -ExecutionPolicy Bypass -File sign_installer.ps1 -ExePath "%SRCDIR%\FeeHunt.exe"
set "SIGN_APP_RC=%errorlevel%"
if "%SIGN_APP_RC%"=="1" ( echo ERROR: signing inner FeeHunt.exe failed. & exit /b 1 )

REM --- 6. Inno Setup compile ---
echo [6/7] Compiling installer with Inno Setup...
if not exist "%ISCC%" ( echo ERROR: ISCC.exe not found at "%ISCC%" & exit /b 1 )
"%ISCC%" /DMyAppVersion=%VERSION% "/DSourceDir=%SRCDIR%" FeeHuntSetup.iss
if errorlevel 1 ( echo ERROR: Inno Setup compile failed & exit /b 1 )

set "INSTALLER=dist_installer\FeeHunt-Setup-v%VERSION%.exe"

REM --- 7. Code-sign the installer (SSL.com eSigner CodeSignTool) ---
echo [7/7] Signing installer (you will be prompted for SSL.com password + TOTP)...
powershell -NoProfile -ExecutionPolicy Bypass -File sign_installer.ps1 -ExePath "%INSTALLER%"
set "SIGN_RC=%errorlevel%"
if "%SIGN_RC%"=="1" ( echo ERROR: code signing failed. & exit /b 1 )

echo.
echo === DONE ===
echo Installer: %INSTALLER%
if "%SIGN_RC%"=="2" (
  echo WARNING: CodeSignTool not found - app exe and installer are UNSIGNED.
  echo          Install CodeSignTool and set CODE_SIGN_TOOL_PATH, then run:
  echo          powershell -ExecutionPolicy Bypass -File sign_installer.ps1 -ExePath "%INSTALLER%"
) else (
  echo Status   : inner FeeHunt.exe + installer SIGNED ^& verified.
)
echo.
endlocal
