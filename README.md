Calculadora Python
Este é um projeto de uma calculadora simples, desenvolvida em Python, com uma interface gráfica usando o Tkinter. A calculadora realiza operações matemáticas básicas, como soma, subtração, multiplicação e divisão.

Funcionalidades
Soma

Subtração

Multiplicação

Divisão

A calculadora foi empacotada em um instalador usando Inno Setup, permitindo que os usuários instalem facilmente a aplicação em seus sistemas Windows.

Como Instalar
Download do Instalador:

Você pode baixar o instalador da calculadora em link para o instalador.

Executar o Instalador:

Após o download, clique duas vezes no arquivo .exe para iniciar a instalação.

Seguir as Instruções:

O instalador guiará você através do processo de instalação. Escolha o diretório de instalação desejado e clique em Instalar.

Iniciar a Calculadora:

Após a instalação, você pode abrir a calculadora a partir do menu Iniciar ou clicando no ícone da área de trabalho.

Como Usar
Abrir a Calculadora:

Após a instalação, abra a aplicação clicando no ícone da calculadora na área de trabalho ou no menu iniciar.

Realizar Operações:

A interface é simples. Digite os números e use os botões para realizar as operações.

Exemplo: Para calcular 3 + 4, digite 3, clique no botão de soma (+), e depois clique em 4. O resultado será mostrado na tela.

Como Criar o Instalador (Inno Setup)
Caso você queira criar seu próprio instalador usando o Inno Setup, siga as instruções abaixo:

Instalar o Inno Setup:

Baixe e instale o Inno Setup.

Configuração do Script:

Crie um script do Inno Setup para o instalador, com base nos arquivos do projeto. Um exemplo básico de script pode ser:

ini
Copiar
Editar
[Setup]
AppName=Calculadora Python
AppVersion=1.0
DefaultDirName={pf}\CalculadoraPython
DefaultGroupName=Calculadora Python
OutputDir=.\Output
OutputBaseFilename=calculadora_installer
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\calculadora.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\calcscripts.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\calc_functions.py"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Calculadora Python"; Filename: "{app}\calculadora.exe"

[Run]
Filename: "{app}\calculadora.exe"; Description: "Iniciar Calculadora"; Flags: nowait postinstall skipifsilent
Criar o Instalador:

Após configurar o script, execute o Inno Setup e compile o instalador. O instalador gerado estará na pasta Output.

Contribuindo
Se você quiser contribuir para o projeto, siga os seguintes passos:

Faça um fork deste repositório.

Crie uma nova branch (git checkout -b feature-nome-da-feature).

Faça suas alterações e envie um pull request.

