#define MyAppName "FeeHunt"
#define MyAppVersion "1.6"
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
OutputBaseFilename=FeeHunt-Setup-v1.6
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayName=FeeHunt
UninstallDisplayIcon={app}\{#MyAppExeName}
VersionInfoVersion=1.6.0.0
VersionInfoCompany=FeeHunt
VersionInfoDescription=FeeHunt Setup Installer
VersionInfoProductName=FeeHunt
VersionInfoProductVersion=1.6
#ifexist "icon.ico"
SetupIconFile=icon.ico
#endif

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "dist\FeeHunt\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "token.json,last_scan_results.json,feehunt_settings.json,feehunt_rules.json,feehunt_license.json"

[Icons]
Name: "{group}\FeeHunt"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\{#MyAppExeName}"
Name: "{group}\Uninstall FeeHunt"; Filename: "{uninstallexe}"
Name: "{autodesktop}\FeeHunt"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\{#MyAppExeName}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch FeeHunt"; Flags: nowait postinstall skipifsilent
