from ollama import chat
from ollama import ChatResponse
import re
import random

#sed = random.randint(0,2511715)
sed = 871521

stream = chat(
  model='robo.micro9',
  messages=[{'role': 'user', 'content': "Explique a história da final da copa do mundo de 2014. Destacando os jogos que o Brasil ganhou antes de ir para a final"}],
  stream=True,
  think=False,
  options={"seed":sed}
)

fullMsg = ""
frase = ""

emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F900-\U0001FAF0"  # emoticons
        u"\U00002728"  #
        u"\U0001F31F"  #
        u"\U00002763-\U00002764"  #
        u"\U00002B50"  #
        #u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        #u"\U0001F680-\U0001F6FF"  # transport & map symbols
        #u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

try:
  for chunk in stream:
    #print(chunk['message']['content'], end='', flush=True)
    fullMsg += chunk['message']['content']
    frase += chunk['message']['content']
    if '.' in chunk['message']['content']:
      emotion = emoji_pattern.findall(frase)
      print({"emocao": (emotion[0] if emotion else "😀"), "texto":emoji_pattern.sub(r'', frase)})
      #print(frase)
      frase = ""
  print(fullMsg)
  print(sed)
except:

  #print(stream["message"]["content"])
  print(fullMsg)