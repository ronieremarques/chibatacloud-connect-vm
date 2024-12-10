@echo off

:: Solicitar permissão de administrador para garantir que o script possa alterar configurações do sistema
powershell -Command "Start-Process cmd -ArgumentList '/c echo Administrador necessário' -Verb RunAs"

:: Mudar o papel de parede da tela inicial
set "wallpaperUrl=https://drive.usercontent.google.com/uc?id=1-DJcn-3FZVxj6EfVbH3rJf48N8rkM09w&export=download"
set "localWallpaperPath=%temp%\chibatacloudwallpaper.png"

:: Baixar a imagem do papel de parede
powershell -command "Invoke-WebRequest -Uri '%wallpaperUrl%' -OutFile '%localWallpaperPath%'"

:: Definir o papel de parede da tela inicial
powershell -Command "Set-ItemProperty -Path 'HKCU:\Control Panel\Desktop' -Name Wallpaper -Value '%localWallpaperPath%'"
powershell -Command "Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public class Wallpaper { [DllImport(\"user32.dll\")] public static extern int SystemParametersInfo(int uAction, int uParam, string lpvParam, int fuWinIni); }'; [Wallpaper]::SystemParametersInfo(20, 0, '%localWallpaperPath%', 3)"

:: Baixar o ícone da pasta
set "iconUrl=https://drive.usercontent.google.com/uc?id=19_uC3WK-GCGyM7EkWoIGCA7H9NqdB6yk&export=download"
set "iconPath=%USERPROFILE%\Documents\Icones\chibatacloud.ico"

:: Baixar o ícone
powershell -command "Invoke-WebRequest -Uri '%iconUrl%' -OutFile '%iconPath%'"

:: Alterar ícones da área de trabalho
set "desktopPath=C:\Users\BCG\Desktop"

:: Alterar ícone para Desktop (720p).bat
powershell -command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%desktopPath%\Desktop (720p).bat.lnk'); $s.IconLocation='%iconPath%'; $s.Save()"

:: Alterar ícone para Desktop (768p).bat
powershell -command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%desktopPath%\Desktop (768p).bat.lnk'); $s.IconLocation='%iconPath%'; $s.Save()"

:: Alterar ícone para Desktop (1080p).bat
powershell -command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%desktopPath%\Desktop (1080p).lnk'); $s.IconLocation='%iconPath%'; $s.Save()"

:: Alterar ícone para Fix Mouse Duplicado
powershell -command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%desktopPath%\Fix Mouse Duplicado.lnk'); $s.IconLocation='%iconPath%'; $s.Save()"

:: Alterar ícone para Start Fix Bug
powershell -command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%desktopPath%\Start Fix Bug.lnk'); $s.IconLocation='%iconPath%'; $s.Save()"

:: Cria um arquivo Alterar Senha.bat na pasta Desktop com o ícone e o conteúdo
echo @echo off > "%desktopPath%\Change Password.bat"
echo cd C:\sunshine >> "%desktopPath%\Change Password.bat"
echo start alterarsenha.exe >> "%desktopPath%\Change Password.bat"

:: Deletar desktop.png da pasta Sunshine\assets
del /F /Q "C:\Program Files\Sunshine\assets\desktop.png" >nul 2>&1

:: Baixar nova imagem para a pasta Sunshine\assets
set "newImageUrl=https://drive.usercontent.google.com/uc?id=1zAQ2H_LanVDAEpSey4aayNAkYtvVmF5h&export=download"
set "newImagePath=C:\Program Files\Sunshine\assets\desktop.png"

:: Baixar a nova imagem com permissões elevadas
powershell -Command "Start-Process powershell -ArgumentList 'Invoke-WebRequest -Uri ''%newImageUrl%'' -OutFile ''%newImagePath%''' -Verb RunAs -WindowStyle Hidden"

:: Remover o arquivo apps.json se existir com permissões elevadas
set "configPath=C:\Program Files\Sunshine\config\apps.json"
powershell -Command "Start-Process powershell -ArgumentList 'Remove-Item -Path ''%configPath%'' -Force' -Verb RunAs -WindowStyle Hidden"

:: Baixar o arquivo JSON com permissões elevadas
set "jsonUrl=https://drive.usercontent.google.com/uc?id=1MnGRlt-6JxFiHPkClhyjHN8KXiw8JUwX&export=download"
set "jsonPath=C:\Program Files\Sunshine\config\apps.json"

:: Baixar o novo arquivo JSON
powershell -Command "Start-Process powershell -ArgumentList 'Invoke-WebRequest -Uri ''%jsonUrl%'' -OutFile ''%jsonPath%''' -Verb RunAs -WindowStyle Hidden"

:: Aguardar o término dos downloads antes de reiniciar o sistema
timeout /t 10 >nul

:: Reiniciar o sistema
shutdown /r /t 0