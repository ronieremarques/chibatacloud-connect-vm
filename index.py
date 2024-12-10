import pyautogui
import asyncio
import pyperclip
import keyboard
import psutil  # Importar psutil para verificar processos
import sys  # Importar sys para acessar os argumentos da linha de comando
import json

# Obter os dados passados como argumentos
if len(sys.argv) < 5:
    print("Uso: python index.py <IP> <Usuário> <Nova Senha> <Senha>")
    sys.exit(1)

ip = sys.argv[1]  # Primeiro argumento: IP
usuario = sys.argv[2]  # Segundo argumento: Usuário
novasenha = sys.argv[3]  # Terceiro argumento: Nova senha
senha = sys.argv[4]  # Quarto argumento: Senha

pyautogui.FAILSAFE = False

# Função para conectar ao RDP
async def conectar_rdp():
    # Primeira execução de conexão
    await conectar()  # Chama a função de conexão inicial
    reconnections = 0  # Contador de reconexões


    while True:  # Loop para verificar se o RDP ainda está em execução
        # Verificar se o processo do RDP está em execução
        rdp_running = any(proc.name() == "mstsc.exe" for proc in psutil.process_iter())
        
        if not rdp_running:
            if reconnections == 0:  # Se ainda não reconectou, tenta reconectar
                await asyncio.sleep(40)  # Esperar 40 segundos antes de tentar conectar novamente
                await conectar2()  # Tenta conectar novamente
                reconnections += 1  # Incrementa o contador de reconexões
            else:
                # Converter a mensagem em JSON válido e encerrar o programa
                print(json.dumps({
                    "message": "conexão bem sucedida",
                    "ipMoonlight": ip,
                    "usuario": usuario,
                    "senha": novasenha
                }))
                sys.exit(0)  # Encerra o programa com código de sucesso
        else:
            await asyncio.sleep(5)  # Esperar um pouco antes de verificar novamente


async def conectar():
    pyautogui.hotkey('win', 'r')  # Chama a função para abrir a janela Executar
    await asyncio.sleep(2)  # Aguarde um pouco
    keyboard.write("mstsc")
    await asyncio.sleep(2)  # Aguarde um pouco
    keyboard.press_and_release('enter')
    await asyncio.sleep(2)  # Aguarde a janela de conexão abrir

    keyboard.write(ip)

    await asyncio.sleep(2)
    pyautogui.click(x=523, y=349)

    # Digitar o nome de usuário
    await asyncio.sleep(2)  # Aguarde um pouco
    pyautogui.press('tab')
    await asyncio.sleep(2)  # Aguarde um pouco
    keyboard.write(usuario)
    await asyncio.sleep(2)  # Aguarde um pouco
    keyboard.press_and_release('enter')
    await asyncio.sleep(5)  # Aguarde um pouco

    # Colar a senha
    await copiar_e_colar(senha.replace('"', ''))  # Usar a biblioteca pyperclip para copiar a senha
    await asyncio.sleep(2)  # Aguarde um pouco após colar
    keyboard.press_and_release('enter')  # Pressionar Enter para conectar
    await asyncio.sleep(5)  # Aguarde a conexão ser estabelecida

    # Confirmar o certificado, se necessário
    pyautogui.hotkey('alt', 'tab')
    await asyncio.sleep(2)  # Aguarde um pouco após colar
    pyautogui.press('left')
    await asyncio.sleep(2)  # Aguarde um pouco
    keyboard.press_and_release('enter')  # Pressionar Enter para confirmar
    await asyncio.sleep(120)  # Aguarde a confirmação

    # Digitar senha
    keyboard.write(novasenha)  # Usar a nova senha aqui também
    await asyncio.sleep(2)  # Aguarde um pouco
    pyautogui.press('enter')
    await asyncio.sleep(2)  # Aguarde um pouco
    # Simular Windows + R
    pyautogui.hotkey('win', 'r')  # Chama a função para abrir a janela Executar
    await asyncio.sleep(2)  # Aguarde a janela Executar abrir

    # Digitar 'cmd' e pressionar Enter
    keyboard.write('cmd')
    await asyncio.sleep(2)  # Aguarde um pouco
    keyboard.press_and_release('enter')
    await asyncio.sleep(2)  # Aguarde o terminal abrir

    keyboard.write('powershell -Command "Invoke-WebRequest -Uri "')

    await asyncio.sleep(2)  # Aguarde a janela de conexão abrir
    keyboard.write('https://encurtador.com.br/REE2o')
    await asyncio.sleep(2)  # Aguarde a janela de conexão abrir
    keyboard.write('" -OutFile "script.bat"')
    await asyncio.sleep(2)  # Aguarde a janela de conexão abrir
    keyboard.press_and_release('enter')  # Pressionar Enter para executar o comando
    await asyncio.sleep(2)  # Aguarde um pouco
    keyboard.write('script.bat')
    await asyncio.sleep(2)  # Aguarde um pouco
    keyboard.press_and_release('enter')

async def conectar2():
    pyautogui.hotkey('win', 'r')
    await asyncio.sleep(2)  # Aguarde a janela de conexão abrir  # Chama a função para abrir a janela Executar
    keyboard.write('mstsc')
    await asyncio.sleep(2)  # Aguarde a janela de conexão abrir
    keyboard.press_and_release('enter')
    await asyncio.sleep(2)  # Aguarde a janela de conexão abrir

    keyboard.write(ip)

    await asyncio.sleep(2)
    pyautogui.click(x=523, y=349)

    await asyncio.sleep(2)
    pyautogui.press('tab')
    await asyncio.sleep(2)
    keyboard.write(usuario)
    await asyncio.sleep(2)
    keyboard.press_and_release('enter')
    await asyncio.sleep(5)  # Aguarde um pouco

    # Colar a senha
    keyboard.write(novasenha)
    await asyncio.sleep(2)  # Aguarde um pouco após colar
    keyboard.press_and_release('enter')  # Pressionar Enter para conectar
    await asyncio.sleep(5)  # Aguarde a conexão ser estabelecida

    # Confirmar o certificado, se necessário
    pyautogui.hotkey('alt', 'tab')
    await asyncio.sleep(2)  # Aguarde um pouco após colar
    pyautogui.press('left')
    await asyncio.sleep(2)
    keyboard.press_and_release('enter')  # Pressionar Enter para confirmar
    await asyncio.sleep(20)  # Aguarde a confirmação

    pyautogui.click(x=934, y=7)
    await asyncio.sleep(2)
    keyboard.press_and_release('enter')

async def copiar_e_colar(copy):
    pyperclip.copy(copy)  # Copia o texto para a área de transferência
    await asyncio.sleep(2)
    keyboard.press_and_release('ctrl+v')

async def colar():
    keyboard.press_and_release('ctrl+v')

# Executar a função
asyncio.run(conectar_rdp())
