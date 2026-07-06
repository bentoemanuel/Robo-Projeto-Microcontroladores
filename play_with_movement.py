import time
import numpy as np
from scipy.io import wavfile
import sounddevice as sd
import asyncio
import serial


def enviar_para_arduino(porta_serial, intensidade_float: float):
    comando = f"{intensidade_float:.2f}\n".encode('utf-8')
    print(comando)
    porta_serial.write(comando)

def get_mouth_positions(filepath, block_size=0.1):
    bitrate, data = wavfile.read(filepath)

    # converts to mono if stereo
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)

    samples_per_part = int(bitrate * block_size)
    total_parts = len(data) // samples_per_part

    pos = []

    for i in range(total_parts):
        beg = i * samples_per_part
        end = beg + samples_per_part
        block = data[beg:end].astype(np.float64)
        # Root Mean Square calculates the energy of the audio block
        rms = np.sqrt(np.mean(block**2)) 
        pos.append(rms)

    max_rms = np.max(pos)
    if max_rms > 0:
        pos = pos / max_rms

    return pos.tolist()

def emocao_int(emocao: str): 
    if emocao in "😛🤠🫡🙃🫠🤐😐😶🫥😶‍🌫️🤥🫨😷🥵🥶😗🥲":
        return 1
    elif emocao in "😉😜":
        return 2
    elif emocao in "🥺🥹":
        return 3
    elif emocao in "😱😨":
        return 4
    elif emocao in "🤪🥴😵‍💫":
        return 5
    elif emocao in "😝😆😂🤣":
        return 6
    elif emocao in "🤑":
        return 7
    elif emocao in "🤨":
        return 8
    elif emocao in "🤗🤭😋🥳🥰😙😚☺️😇😄😅":
        return 9
    elif emocao in "🤔🧐🥸":
        return 10
    elif emocao in "🤩✨💫⭐🌟":
        return 11
    elif emocao in "😡🤬😠":
        return 12
    elif emocao in "🤤🥱":
        return 13
    elif emocao in "😎":
        return 14
    elif emocao in "🤓":
        return 15
    elif emocao in "😑🫩":
        return 16
    elif emocao in "😒😏":
        return 17
    elif emocao in "🙄":
        return 18
    elif emocao in "😭":
        return 19
    elif emocao in "😬🤫🫢🫣🤯😲":
        return 20
    elif emocao in "😮‍💨🙂‍↔️🙂‍↕️😌😔😪😴":
        return 21
    elif emocao in "🤒🤕":
        return 22
    elif emocao in "🤢🤮🤧😣😫😓😖😩😤":
        return 23
    elif emocao in "😍❤️😘💕":
        return 24
    elif emocao in "😵":
        return 25
    elif emocao in "👀":
        return 26
    else:
        return 1

async def play_and_sync_mouth(porta_serial, filepath, emotion, block_size=0.1):
    """
    Plays the audio file in the background and prints the normalized 
    energy level every block_size seconds.
    """
    positions = get_mouth_positions(filepath, block_size)
    bitrate, data = wavfile.read(filepath)
    

    emocao_n = str(emocao_int(emotion))
    print(f"emocao n = {emocao_n}")
    porta_serial.write("C\n".encode('utf-8'))
    for part in emocao_n:
        print(f"emocao part = {part}")
        porta_serial.write(f"{part}\n".encode('utf-8'))
    porta_serial.write("D\n".encode('utf-8'))


    sd.play(data, bitrate)
    start_time = time.time()

    for i, energy in enumerate(positions):
        target_time = start_time + (i * block_size)
        current_time = time.time()
        
        # Calculate how long we need to wait until the target time
        sleep_duration = target_time - current_time
        
        # Sleep only if we haven't already passed the target time
        if sleep_duration > 0:
            await asyncio.sleep(sleep_duration)

        enviar_para_arduino(porta_serial, energy)

        
    sd.wait()


