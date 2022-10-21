#!/usr/bin/env python3

import argparse
import queue
import sys
import sounddevice as sd
import text_to_speech_pyttsx3
import time

from vosk import Model, KaldiRecognizer

q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    "-l", "--list-devices", action="store_true",
    help="show list of audio devices and exit")
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    "-f", "--filename", type=str, metavar="FILENAME",
    help="audio file to store recording to")
parser.add_argument(
    "-d", "--device", type=int_or_str,
    help="input device (numeric ID or substring)")
parser.add_argument(
    "-r", "--samplerate", type=int, help="sampling rate")
args = parser.parse_args(remaining)

try:
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, "input")
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info["default_samplerate"])

    model = Model(lang="en-us")

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device,
            dtype="int16", channels=1, callback=callback):
        print("#" * 80)
        print("Press Ctrl+C to stop the recording")
        print("#" * 80)

        rec = KaldiRecognizer(model, args.samplerate)
        bill_called = 0
        listen_question = 0
        text_to_speech_pyttsx3.runSoundFIle("Hello, I'm Bill")

        time_end = 0

        while True:
            data = q.get()
            #print(type)

            # Variável que determina se uma questão foi feita ou não(caso não seja feita vira 1)
            no_question = 0
            
            # Limpa o cache de palavras detectadas(ocorre quando fica muito tempo sem ouvir nada)
            if rec.AcceptWaveform(data):
                rec.Result()
            else:
                # Verifica se a frase "Okay Bill" foi dita.(Se sim, a variável bill_called fica 1 e a verificação não é feita novamente)
                if "okay" in rec.PartialResult() and "b" in rec.PartialResult() or bill_called:
                    if not listen_question:
                        text_to_speech_pyttsx3.runSoundFIle("Hello! Are you up for some questions?")

                        # Variável não permite que Okay bill seja chamada duas vezes antes de 10 segundos
                        listen_question = 1
                        
                        #time handling (10 for 10 seconds)
                        time_end = time.time() + 10
                    
                    # Variável recebe 1 quando bill é chamado
                    bill_called = 1

                    # Estrutura de pergunta, somente substantivos, verbos e adjetivos são considerados, verificando se eles estão dentro da string
                    if "what" in rec.PartialResult() and "oldest" in rec.PartialResult() and "sta" in rec.PartialResult() and "brazil" in rec.PartialResult():
                        
                        text_to_speech_pyttsx3.runSoundFIle("Pernambuco")
                        bill_called = 0
                        listen_question = 0
                    elif "what" in rec.PartialResult() and "newest" in rec.PartialResult() and "sta" in rec.PartialResult() and "brazil" in rec.PartialResult():
                        text_to_speech_pyttsx3.runSoundFIle("Tocantins")
                        bill_called = 0
                        listen_question = 0
                    elif "what" in rec.PartialResult() and "capital" in rec.PartialResult() and "rio grande" in rec.PartialResult() and ("so" in rec.PartialResult() or "sul" in rec.PartialResult()):
                        text_to_speech_pyttsx3.runSoundFIle("Porto Alegre")
                        bill_called = 0
                        listen_question = 0
                    elif "what" in rec.PartialResult() and "you" in rec.PartialResult() and "eat" in rec.PartialResult() and "lunch" in rec.PartialResult():
                        text_to_speech_pyttsx3.runSoundFIle("I had a byte")
                        bill_called = 0
                        listen_question = 0
                    elif "what" in rec.PartialResult() and "you" in rec.PartialResult() and "eat" in rec.PartialResult() and "lunch" in rec.PartialResult():
                        text_to_speech_pyttsx3.runSoundFIle("I had a byte")
                        bill_called = 0
                        listen_question = 0
                    elif "what" in rec.PartialResult() and "acronym" in rec.PartialResult() and "g" in rec.PartialResult() and ("n" in rec.PartialResult() or "and" in rec.PartialResult()) and ("u" in rec.PartialResult() or "you" in rec.PartialResult()) and "present" in rec.PartialResult():
                        text_to_speech_pyttsx3.runSoundFIle("GNU is a recursive acronym meaning GNU is not Unix")
                        bill_called = 0
                        listen_question = 0
                    elif "why" in rec.PartialResult() and "chicken" in rec.PartialResult() and "road" in rec.PartialResult():
                        text_to_speech_pyttsx3.runSoundFIle("What if the road is only a construct of the chickens mind")
                        #while True:
                        #    data = q.get()
                        #    if rec.AcceptWaveform(data):
                        #        rec.Result()
                        #    else:
                        #        if "what" in rec.PartialResult() and "chic" in rec.PartialResult() and "only" in rec.PartialResult() and "cons" in rec.PartialResult() and "road" in rec.PartialResult() and "mind" in rec.PartialResult():
                        #            text_to_speech_pyttsx3.runSoundFIle("What if the chicken and the road are only a consstruct of your mind")
                        #            break
                        #    print(rec.PartialResult())
                        bill_called = 0
                        listen_question = 0
                    #if time's up
                    elif time.time() >= time_end and time_end != -1:
                        listen_question = 0
                        
                        bill_called = 0
                        
                        # Questão não foi respondida e recebe 1
                        no_question = 1
                        
                        time_end = -1
                
                # Se a questão for respondida em 10s não entra nesse if , caso contrário entra no if e fala que não entendeu a questão 
                if no_question:
                    text_to_speech_pyttsx3.runSoundFIle("Sorry, I didnt understood the question")
                    no_question = 0
                if '""' not in rec.PartialResult():
                    print(rec.PartialResult())
                
            if dump_fn is not None:
                dump_fn.write(data)

except KeyboardInterrupt:
    print("\nDone")
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ": " + str(e))
