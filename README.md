# Robo-Projeto-Microcontroladores

Esse é um projeto de um robô conversador com integração com Arduino.
A cada iteração, ele segue esses passsos:
1. Grava um áudio;
2. Transcreve ele usando o modelo local whisper-small;
3. Passa para uma LLM local, que gera uma resposta;
4. Usa um modelo TTS para gerar o áudio da resposta;
5. Para cada áudio que fica pronto, envia pela serial as intensidades para cada janela do áudio, junto com os comandos associados à emoção (1 por frase) obtidas na resposta da LLM.

## Arquitetura

## Dependências

## Como usar
1. Rodar o código em main.py
2. Apertar o botão "Gravar áudio" na interface
3. 
