#define MyAppName "FeeHunt"
#define MyAppVersion "1.12.4"
#define MyAppPublisher "FeeHunt"
#define MyAppURL "https://feehunt.pro"
#define MyAppExeName "FeeHunt.exe"

[Setup]
AppId={{C1DA4E73-3CF1-4CB6-8C9B-28E0C0B0D7E3}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\FeeHunt
DefaultGroupName=FeeHunt
DisableProgramGroupPage=yes
OutputDir=dist_installer
OutputBaseFilename=FeeHunt-Setup-v1.12.4
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayName=FeeHunt
UninstallDisplayIcon={app}\{#MyAppExeName}
; Close a running FeeHunt before replacing files, then restart it afterwards.
; Without this, updating while FeeHunt is open fails with
; "DeleteFile failed; code 5. Access is denied." on FeeHunt.exe.
CloseApplications=yes
CloseApplicationsFilter=*.exe,*.dll
RestartApplications=yes
VersionInfoVersion=1.12.4.0
VersionInfoCompany=FeeHunt
VersionInfoDescription=FeeHunt Setup Installer
VersionInfoProductName=FeeHunt
VersionInfoProductVersion=1.12.4
#ifexist "icon.ico"
SetupIconFile=icon.ico
#endif

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "dist_v1124\FeeHunt\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "token.json,last_scan_results.json,feehunt_settings.json,feehunt_rules.json,feehunt_memory.json,feehunt_license.json,feehunt_session.json,.env,.env.txt"

[Icons]
Name: "{group}\FeeHunt"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\{#MyAppExeName}"
Name: "{group}\Uninstall FeeHunt"; Filename: "{uninstallexe}"
Name: "{autodesktop}\FeeHunt"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\{#MyAppExeName}"

[Registry]
; Let feehunt.pro open an already-installed desktop app without sending the
; user back through the installer. The browser may ask for confirmation first.
Root: HKA; Subkey: "Software\Classes\feehunt"; ValueType: string; ValueName: ""; ValueData: "URL:FeeHunt Protocol"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\feehunt"; ValueType: string; ValueName: "URL Protocol"; ValueData: ""
Root: HKA; Subkey: "Software\Classes\feehunt\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"
Root: HKA; Subkey: "Software\Classes\feehunt\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""

[Run]
; runasoriginaluser: the installer runs elevated (PrivilegesRequired=admin), but
; FeeHunt must launch as the normal user. Launching it elevated breaks Streamlit's
; local server handshake ("CallSpawnServer: Unexpected response") and localhost access.
Filename: "{app}\{#MyAppExeName}"; Description: "Launch FeeHunt"; Flags: nowait postinstall skipifsilent runasoriginaluser
