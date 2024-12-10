const express = require('express');
const app = express();
const { spawn } = require('child_process');
const localtunnel = require('localtunnel');

app.get('/', (req, res) => {
    res.send('Hello World');
});

app.get('/preload', async (req, res) => {
    // Executar os comandos de registro antes de chamar o Python
    await new Promise((resolve, reject) => {
        const commands = `
@echo off
reg delete "HKEY_CURRENT_USER\\Software\\Microsoft\\Terminal Server Client\\Default" /va /f
reg delete "HKEY_CURRENT_USER\\Software\\Microsoft\\Terminal Server Client\\Servers" /f
reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Terminal Server Client\\Servers"
del /a /q /s "%userprofile%\\documents\\Default.rdp"
for /f "tokens=1,2 delims==" %%G in ('cmdkey /list ^| findstr /i "TERMSRV"') do cmdkey /delete:%%H
        `;
        exec(commands, (error, stdout, stderr) => {
            if (error) {
                console.error(`Erro: ${error.message}`);
                return reject(error);
            }
            if (stderr) {
                console.error(`Erro: ${stderr}`);
                return reject(new Error(stderr));
            }
            console.log(`Saída: ${stdout}`);
            resolve();
        });
    });

    // Chamar o script Python para conectar e obter os dados
    const pythonProcess = await spawn('python3', ['index.py', ipRDP, usuario, novaSenha, `"${senha}"`]); // Passar IP, usuário e nova senha

    pythonProcess.stdout.on('data', async (data) => {
        const connectionData = JSON.parse(data.toString()); // Parsear os dados recebidos do Python

        res.send(connectionData);

    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Erro: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`Processo Python encerrado com código ${code}`);
    });
});

app.listen(3000, () => {
    localtunnel(3000, { subdomain: 'chibatacloud' }, (err, tunnel) => {
        if (err) {
            console.error('Erro ao criar o tunnel:', err);
        } else {
            console.log('Tunnel criado com sucesso:', tunnel.url);
        }
    });
    console.log('Server is running on port 3000');
});