import pyttsx3
def runSoundFIle (voiced_text):
    audio = pyttsx3.init()
    audio.setProperty('voice','english')
    audio.setProperty('rate', 125)
    audio.setProperty('volume',1)

    audio.say(voiced_text)

    audio.runAndWait()