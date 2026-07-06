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

<img width="3589" height="1963" alt="Untitled Sketch_bb" src="https://github.com/user-attachments/assets/ea8f9b62-db7f-4e4f-b595-89ede69254be" />
