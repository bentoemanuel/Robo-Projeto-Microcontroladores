import asyncio
from kokoro import KPipeline
import soundfile as sf
import tempfile

from play_with_movement import play_and_sync_mouth

pipeline = KPipeline(lang_code='p')

def generator_worker(sentences: list, loop: asyncio.AbstractEventLoop, queue: asyncio.Queue):
    for i, sentence in enumerate(sentences):
        
        generator = pipeline(sentence, voice='pm_alex', speed=1.55)
        
        for gs, ps, audio in generator:
            print(f"[Worker] Áudio gerado: {gs}")
            filename = f'{i}.wav'
            sf.write(filename, audio, 24000)
            
            asyncio.run_coroutine_threadsafe(queue.put(filename), loop)
            
    asyncio.run_coroutine_threadsafe(queue.put(None), loop)

def generator_worker_one_sentence(i: int, sentence: str, emotion: str, loop: asyncio.AbstractEventLoop, queue: asyncio.Queue):
    generator = pipeline(sentence, voice='pm_alex', speed=1.55)
    
    for gs, ps, audio in generator:
        print(f"[Worker] Áudio gerado: {gs}")
        filename = f'{i}.wav'
        sf.write(filename, audio, 24000)
        
        asyncio.run_coroutine_threadsafe(queue.put((filename, emotion)), loop)
        
async def process(text: str):
    loop = asyncio.get_running_loop()
    
    queue = asyncio.Queue()
    
    loop.run_in_executor(None, generator_worker, sentences, loop, queue)
    
    while True:
        result = await queue.get()
        
        if result is None:
            break
            
        print(f"[Player] Tocando {result}...")
        await play_and_sync_mouth(result)

async def process_and_play(text: str):
    sentences = text.split('.')
    loop = asyncio.get_running_loop()
    
    queue = asyncio.Queue()
    
    loop.run_in_executor(None, generator_worker, sentences, loop, queue)
    
    while True:
        result = await queue.get()
        
        if result is None:
            break
            
        print(f"[Player] Tocando {result}...")
        await play_and_sync_mouth(result)


if __name__ == "__main__":
    text = "Este é um teste de geração de áudio em paralelo. Vamos ver se realmente está gerando os arquivos de áudio corretamente. Esse é apenas um teste."
    asyncio.run(process_and_play(text))
    print("Finalizado!")