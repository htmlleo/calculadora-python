[Setup]
AppName=Torre de Hanoi Manual
AppVersion=1.0
AppPublisher=Leonardo Estevão Alves
DefaultDirName={autopf}\Torre de Hanoi Manual
DefaultGroupName=Torre de Hanoi Manual
OutputDir=C:\Users\Léo the fox mestre\Desktop\jogo\instalador
OutputBaseFilename=Instalador_Torre_Hanoi
Compression=lzma
SolidCompression=yes

[Languages]
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"

[Files]
Source: "C:\Users\Léo the fox mestre\Desktop\jogo\dist\jogo.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Torre de Hanoi Manual"; Filename: "{app}\jogo.exe"
Name: "{group}\Desinstalar Torre de Hanoi Manual"; Filename: "{uninstallexe}"
Name: "{userdesktop}\Torre de Hanoi Manual"; Filename: "{app}\jogo.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na Área de Trabalho"; GroupDescription: "Opções adicionais:"; Flags: unchecked

[Run]
Filename: "{app}\jogo.exe"; Description: "Executar o jogo agora"; Flags: nowait postinstall skipifsilent
