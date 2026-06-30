<#
  sign_installer.ps1 - code-sign a Windows .exe with SSL.com eSigner CodeSignTool.

  Contains NO secrets (this repo is public). Configuration is read from, in order:
    1. environment variables
    2. a local untracked file  signing.local.ps1  (gitignored) in the project root
    3. interactive prompt (password + TOTP secret are ALWAYS prompted if not in env)

  Config values:
    SSL_USERNAME         SSL.com account username (email)
    SSL_CREDENTIAL_ID    eSigner credential id (from CodeSignTool get_credential_ids)
    CODE_SIGN_TOOL_PATH  folder containing CodeSignTool.bat (default c:\tmp\CodeSignTool)
    SSL_PASSWORD         SSL.com password        (optional; prompted if absent)
    SSL_TOTP_SECRET      eSigner TOTP secret     (optional; prompted if absent)

  Usage:
    powershell -NoProfile -ExecutionPolicy Bypass -File sign_installer.ps1 -ExePath dist_installer\FeeHunt-Setup-v1.12.6.exe

  Exit codes: 0 = signed & verified, 1 = error, 2 = CodeSignTool missing (skipped, file left unsigned).
#>
param(
    [Parameter(Mandatory = $true)][string]$ExePath
)
$ErrorActionPreference = 'Stop'

# --- load optional local config (gitignored) ---
$localCfg = Join-Path $PSScriptRoot 'signing.local.ps1'
if (Test-Path $localCfg) { . $localCfg }

function Get-Conf($name, $default) {
    $v = [Environment]::GetEnvironmentVariable($name)
    if ([string]::IsNullOrWhiteSpace($v)) { return $default } else { return $v }
}
function Read-Secret($label) {
    $sec = Read-Host $label -AsSecureString
    $b = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($sec)
    try { [Runtime.InteropServices.Marshal]::PtrToStringBSTR($b) }
    finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($b) }
}

$toolPath = Get-Conf 'CODE_SIGN_TOOL_PATH' 'c:\tmp\CodeSignTool'
$user     = Get-Conf 'SSL_USERNAME' ''
$cred     = Get-Conf 'SSL_CREDENTIAL_ID' ''
$bat      = Join-Path $toolPath 'CodeSignTool.bat'

if (-not (Test-Path $ExePath)) { Write-Host "[sign] File not found: $ExePath" -ForegroundColor Red; exit 1 }
if (-not (Test-Path $bat)) {
    Write-Host "[sign] CodeSignTool not found at '$toolPath' -> SKIPPING signing; installer left UNSIGNED." -ForegroundColor Yellow
    Write-Host "[sign] Set CODE_SIGN_TOOL_PATH (or signing.local.ps1) to enable signing." -ForegroundColor Yellow
    exit 2
}
if ([string]::IsNullOrWhiteSpace($user)) { $user = Read-Host 'SSL.com username (email)' }
if ([string]::IsNullOrWhiteSpace($cred)) { $cred = Read-Host 'SSL.com eSigner credential_id' }

$pw   = Get-Conf 'SSL_PASSWORD' ''
$totp = Get-Conf 'SSL_TOTP_SECRET' ''
if ([string]::IsNullOrWhiteSpace($pw))   { $pw   = Read-Secret 'SSL.com password (hidden)' }
if ([string]::IsNullOrWhiteSpace($totp)) { $totp = Read-Secret 'SSL.com TOTP secret (hidden)' }

# CodeSignTool.bat honors CODE_SIGN_TOOL_PATH so it can run from any CWD
$env:CODE_SIGN_TOOL_PATH = $toolPath

$exeFull = (Resolve-Path $ExePath).Path
$exeName = [System.IO.Path]::GetFileName($exeFull)
$tmpOut  = Join-Path ([System.IO.Path]::GetDirectoryName($exeFull)) '_signed_tmp'
if (Test-Path $tmpOut) { Remove-Item $tmpOut -Recurse -Force }
New-Item -ItemType Directory -Force $tmpOut | Out-Null

$signed = Join-Path $tmpOut $exeName
$rc = 1
for ($attempt = 1; $attempt -le 2; $attempt++) {
    Write-Host "[sign] Signing $exeName (attempt $attempt) ..." -ForegroundColor Cyan
    & $bat sign "-credential_id=$cred" "-username=$user" "-password=$pw" "-totp_secret=$totp" "-input_file_path=$exeFull" "-output_dir_path=$tmpOut"
    $rc = $LASTEXITCODE
    if ($rc -eq 0 -and (Test-Path $signed)) { break }
    if ($attempt -lt 2) {
        # Most common transient cause is reusing a TOTP code within the same 30s window
        # (e.g. signing several files in one build). Wait for a fresh window, then retry.
        Write-Host "[sign] Signing failed (exit $rc). Waiting 35s for a fresh OTP window, then retrying..." -ForegroundColor Yellow
        Start-Sleep -Seconds 35
        if (Test-Path $tmpOut) { Remove-Item $tmpOut -Recurse -Force -ErrorAction SilentlyContinue }
        New-Item -ItemType Directory -Force $tmpOut | Out-Null
    }
}

if ($rc -ne 0 -or -not (Test-Path $signed)) {
    Write-Host "[sign] CodeSignTool failed (exit $rc) - file NOT signed." -ForegroundColor Red
    Remove-Item $tmpOut -Recurse -Force -ErrorAction SilentlyContinue
    exit 1
}

Copy-Item $signed $exeFull -Force
Remove-Item $tmpOut -Recurse -Force -ErrorAction SilentlyContinue

$sig = Get-AuthenticodeSignature $exeFull
Write-Host "[sign] Status: $($sig.Status)  Signer: $($sig.SignerCertificate.Subject)" -ForegroundColor Green
if ($sig.Status -ne 'Valid') { Write-Host "[sign] WARNING: signature is not Valid!" -ForegroundColor Red; exit 1 }
Write-Host "[sign] OK - $exeName signed and verified." -ForegroundColor Green
exit 0
