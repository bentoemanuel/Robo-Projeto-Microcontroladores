import sys
import queue
import asyncio
import sounddevice as sd
import soundfile as sf
import keyboard
from transformers import pipeline, logging
from ollama import AsyncClient
from ollama import ChatResponse
import re
from tts import generator_worker_one_sentence
from play_with_movement import play_and_sync_mouth
import serial
import time

porta_serial = serial.Serial('COM16', 9600)
time.sleep(2)

logging.set_verbosity(50)
pipe = pipeline("automatic-speech-recognition", model="openai/whisper-small")

# Removemos a inicialização global do client para instanciá-lo dentro do loop principal
message_history = []

def gravar_audio():
    # Configuration settings
    SAMPLE_RATE = 16000
    CHANNELS = 1
    FILENAME = "output_unlimited.wav"

    audio_queue = queue.Queue()

    def audio_callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        audio_queue.put(indata.copy())

    porta_serial.write("A\n".encode('utf-8'))
    print("Recording... Press C to STOP.")

    with sf.SoundFile(FILENAME, mode='w', samplerate=SAMPLE_RATE, channels=CHANNELS) as file:
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=audio_callback):
            while True:
                file.write(audio_queue.get())
                try:
                    if keyboard.is_pressed('c'):
                        print("\nRecording stopped by user. File saved safely.")
                        porta_serial.write("B\n".encode('utf-8'))
                        break
                except:
                    break
                    
    print("Carregando...")
    result = pipe(FILENAME, return_timestamps=True, language="pt")
    return result["text"] if result else None

emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F900-\U0001FAF0"
        u"\U00002728"
        u"\U0001F31F"
        u"\U00002763-\U00002764"
        u"\U00002B50"
                        "]+", flags=re.UNICODE)

def formatar_frase(frase):
    emotion = emoji_pattern.findall(frase)
    return ({"emocao": (emotion[0][0] if emotion else "😀"), "texto":re.sub(r'[^\w\s]', '', strip_emojis(frase))})

def strip_emojis(text: str) -> str:
    return emoji_pattern.sub('', text)

def falar(frasein, i, loop, fila):
    txt = formatar_frase(frasein)
    print(txt)
    task = loop.run_in_executor(None, generator_worker_one_sentence, i, txt["texto"], txt["emocao"], loop, fila)
    return task

async def play_audios(fila):
    while True:
        result = await fila.get()
        if result is None: break
            
        print(f"[Player] Tocando {result[0]} com emocao {result[1]}...")
        await play_and_sync_mouth(porta_serial, result[0], result[1])

async def gerar_resposta(texto, client):
    stream = await client.chat(
        model='robo.micro9',
        messages=message_history,
        stream=True,
        think=False,
        options={"seed":871521}
    )

    print("Gerando resposta...")

    fullMsg = ""
    frase = ""

    fila = asyncio.Queue()
    loop = asyncio.get_running_loop()

    player_task = asyncio.create_task(play_audios(fila))

    i = 0
    tts_tasks = []

    try:
        async for chunk in stream:
            fullMsg += chunk['message']['content']
            frase += chunk['message']['content']
            if '.' in chunk['message']['content']:
                tts_tasks.append(falar(frase, i, loop, fila))
                frase = ""
                i += 1
                
        if frase != "":
            tts_tasks.append(falar(frase, i, loop, fila))

        message_history.append({"role": "assistant", "content": fullMsg})
        print(fullMsg)

        if tts_tasks:
            await asyncio.gather(*tts_tasks)
            
        await fila.put(None)
        await player_task

    except Exception as e:
        print(f"Erro! {e}")

async def main():
    client = AsyncClient()
    
    while True:
        prompt = await asyncio.to_thread(gravar_audio)
        if prompt:
            print(f"Prompt: {prompt}")
            message_history.append({'role': 'user', 'content': prompt})
            await gerar_resposta(prompt, client)

if __name__=="__main__":
    asyncio.run(main())