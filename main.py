import sys
import queue
import asyncio
import sounddevice as sd
import soundfile as sf
from transformers import pipeline, logging
from ollama import AsyncClient
import re
from tts import generator_worker_one_sentence
from play_with_movement import play_and_sync_mouth
import serial
import time
import tkinter as tk
from tkinter import scrolledtext
import threading

porta_serial = serial.Serial('COM16', 9600)
time.sleep(2)

logging.set_verbosity(50)
pipe = pipeline("automatic-speech-recognition", model="openai/whisper-small")

message_history = []

def gravar_audio(app):
    app.start_event.wait()
    
    SAMPLE_RATE = 16000
    CHANNELS = 1
    FILENAME = "output_unlimited.wav"
    audio_queue = queue.Queue()

    def audio_callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        audio_queue.put(indata.copy())

    porta_serial.write("A\n".encode('utf-8'))
    print("Recording...")

    with sf.SoundFile(FILENAME, mode='w', samplerate=SAMPLE_RATE, channels=CHANNELS) as file:
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=audio_callback):
            while app.is_recording:
                try:
                    file.write(audio_queue.get(timeout=0.1))
                except queue.Empty:
                    continue
                    
    print("\nRecording stopped by user. File saved safely.")
    porta_serial.write("B\n".encode('utf-8'))
                    
    print("Carregando (Whisper)...")
    app.escrever_no_chat("\n[Sistema: Transcrevendo seu áudio...]\n")
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

def falar(frasein, i, loop, fila, voz):
    txt = formatar_frase(frasein)
    print(txt)
    task = loop.run_in_executor(None, generator_worker_one_sentence, i, txt["texto"], txt["emocao"], loop, fila, voz)
    return task

async def play_audios(fila, app):
    while True:
        result = await fila.get()
        if result is None: break
        
        app.escrever_no_chat(result[0])

        print(f"[Player] Tocando {result[1]} com emocao {result[2]}...")
        await play_and_sync_mouth(porta_serial, result[1], result[2])

async def gerar_resposta(texto, client, app):
    stream = await client.chat(
        model='robo.micro11',
        messages=message_history,
        stream=True,
        think=False,
        options={"seed":871521}
    )

    print("Gerando resposta...")
    app.escrever_no_chat("\nRobô: ")

    fullMsg = ""
    frase = ""

    fila = asyncio.Queue()
    loop = asyncio.get_running_loop()

    player_task = asyncio.create_task(play_audios(fila, app))

    i = 0
    tts_tasks = []
    
    voz_selecionada = app.voz_var.get()

    try:
        async for chunk in stream:
            pedaco = chunk['message']['content']
            fullMsg += pedaco
            frase += pedaco
                        
            if '.' in pedaco:
                tts_tasks.append(falar(frase, i, loop, fila, voz_selecionada))
                frase = ""
                i += 1
                
        if frase != "":
            tts_tasks.append(falar(frase, i, loop, fila, voz_selecionada))

        message_history.append({"role": "assistant", "content": fullMsg})
        app.escrever_no_chat("\n")
        print(fullMsg)

        if tts_tasks:
            await asyncio.gather(*tts_tasks)
            
        await fila.put(None)
        await player_task

    except Exception as e:
        print(f"Erro! {e}")
        app.escrever_no_chat(f"\n[Erro: {e}]\n")

async def loop_principal_robo(root, app):
    client = AsyncClient()
    
    while True:
        try:
            prompt = await asyncio.to_thread(gravar_audio, app)
            
            if prompt:
                print(f"Prompt: {prompt}")
                app.escrever_no_chat(f"\nVocê: {prompt}\n")
                message_history.append({'role': 'user', 'content': prompt})
                await gerar_resposta(prompt, client, app)
                if "chau" in prompt.lower():
                    porta_serial.write("C\n".encode('utf-8'))
                    porta_serial.write("2\n".encode('utf-8'))
                    porta_serial.write("D\n".encode('utf-8'))
                    await asyncio.sleep(1)
                    porta_serial.write("E\n".encode('utf-8'))
                    root.destroy()
            app.master.after(0, app.reset_botao_gravar)
        except Exception as e:
            print(f"Erro! {e}")
            app.escrever_no_chat(f"\n[Erro: {e}]\n")


def iniciar_thread_asyncio(root, app):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(loop_principal_robo(root, app))

class InterfaceRobo:
    def __init__(self, master):
        self.master = master
        self.master.title("Painel do Robô")
        
        self.is_recording = False
        self.start_event = threading.Event()
        
        frame_config = tk.Frame(master)
        frame_config.pack(pady=10, padx=10, fill=tk.X)
        
        self.btn_gravar = tk.Button(frame_config, text="Gravar Áudio", font=("Arial", 10, "bold"), command=self.toggle_gravacao, width=15)
        self.btn_gravar.pack(side=tk.LEFT, padx=10)
        
        tk.Label(frame_config, text="Voz:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        self.voz_var = tk.StringVar(value="pm_alex")
        tk.Radiobutton(frame_config, text="Alex", variable=self.voz_var, value="pm_alex").pack(side=tk.LEFT)
        tk.Radiobutton(frame_config, text="Dora", variable=self.voz_var, value="pf_dora").pack(side=tk.LEFT)
        
        tk.Label(master, text="Histórico de Chat:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
        self.caixa_texto = scrolledtext.ScrolledText(master, state='disabled', width=80, height=25, font=("Arial", 11), wrap=tk.WORD)
        self.caixa_texto.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    def toggle_gravacao(self):
        if not self.is_recording:
            self.is_recording = True
            self.btn_gravar.config(text="Parar Gravação", bg="red", fg="white")
            self.start_event.set()
        else:
            self.is_recording = False
            self.btn_gravar.config(text="Aguarde...", bg="gray", fg="black", state="disabled")
            
    def reset_botao_gravar(self):
        self.start_event.clear()
        self.btn_gravar.config(text="Gravar Áudio", bg="SystemButtonFace", fg="black", state="normal")
        
    def escrever_no_chat(self, texto):
        self.master.after(0, self._inserir_texto, texto)
        
    def _inserir_texto(self, texto):
        self.caixa_texto.config(state='normal')
        self.caixa_texto.insert(tk.END, texto)
        self.caixa_texto.see(tk.END)
        self.caixa_texto.config(state='disabled')

if __name__=="__main__":
    root = tk.Tk()
    app = InterfaceRobo(root)
    
    thread_robo = threading.Thread(target=iniciar_thread_asyncio, args=(root,app,), daemon=True)
    thread_robo.start()
    
    root.mainloop()