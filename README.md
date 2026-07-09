# Robo-Projeto-Microcontroladores

Esse é um projeto de um robô conversador com integração com Arduino.
A cada iteração, ele segue esses passos:
1. Grava um áudio;
2. Transcreve ele usando o modelo local whisper-small;
3. Passa para uma LLM local, que gera uma resposta;
4. Usa um modelo TTS para gerar o áudio da resposta;
5. Para cada áudio que fica pronto, envia pela serial as intensidades para cada janela do áudio, junto com os comandos associados à emoção (1 por frase) obtidas na resposta da LLM.

## Arquitetura
Modelos:
- **LLM:** Gemma-4
- **STT:** Whisper-small
- **TTS:** Kokoro-82M

## Dependências
- [Ollama](https://ollama.com/download)
- Python 3.x

## Como usar
1. Faça o upload do código `.ino` para o seu Arduino.
2. Baixe o modelo da LLM no Ollama:
```sh
ollama pull gemma:4b
```
3. Instale as dependências do Python:
```sh
pip install -r requirements.txt
```
4. Rode o código principal
```sh
python main.py
```

## Circuito
<img width="3589" height="1963" alt="Untitled Sketch_bb" src="https://github.com/user-attachments/assets/ea8f9b62-db7f-4e4f-b595-89ede69254be" />
