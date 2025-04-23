[Setup]
AppName=Správce hesel
AppVersion=1.0
DefaultDirName={autopf}\Správce hesel
DefaultGroupName=Správce hesel
OutputDir=C:\Users\janga\dist\installer
OutputBaseFilename=SpravceHeselInstaller
SetupIconFile=C:\Users\janga\dist\ICO\passs.ico
Compression=lzma
SolidCompression=yes
DisableProgramGroupPage=yes
CreateUninstallRegKey=yes

[Files]
Source: "C:\Users\janga\dist\spravce.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\janga\dist\ICO\passs.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{userdesktop}\Správce hesel"; Filename: "{app}\spravce.exe"; IconFilename: "{app}\passs.ico"; Tasks: create_shortcut
Name: "{group}\Správce hesel"; Filename: "{app}\spravce.exe"; IconFilename: "{app}\passs.ico"

[Tasks]
Name: "create_shortcut"; Description: "Přidat zástupce na plochu"; GroupDescription: "Volby"; Flags: unchecked

[VersionInfo]
VerFileInfoVersion=1.0.0.0
VerFileInfoCompanyName=Jan Galba
VerFileInfoFileDescription="Správce hesel"
VerFileInfoFileVersion="1.0.0.0"
VerFileInfoProductName="Správce hesel"
VerFileInfoProductVersion="1.0.0.0"
VerFileInfoLegalCopyright="Copyright © 2025 Jan Galba"
VerFileInfoOriginalFilename="spravce.exe"
