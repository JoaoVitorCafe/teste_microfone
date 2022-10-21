import pyttsx3

#audio = pyttsx3.init()
#print(audio.getProperty('voices'))
#audio.setProperty('voice', voice.id)
#audio.setProperty('rate', 125)
#audio.setProperty('volume',1)
#audio.say(voiced_text)
#audio.runAndWait()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 125)
for voice in voices:
   engine.setProperty('voice', voice.id)  # changes the voice
   print(voice.id)
   engine.say('Why did the chicken cross the road?')
engine.runAndWait()