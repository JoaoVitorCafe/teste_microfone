#!/usr/bin/env python3

import argparse
import queue
import sys
import sounddevice as sd
import text_to_speech_pyttsx3

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
        question_answered = 0
        listen_question = 0
        text_to_speech_pyttsx3.runSoundFIle("Hello, I'm Bill")
        while True:
            data = q.get()
            #print(type)
            if rec.AcceptWaveform(data):
                rec.Result()
            else:
                if "okay" in rec.PartialResult() and "b" in rec.PartialResult() or question_answered:
                    if not listen_question:
                        text_to_speech_pyttsx3.runSoundFIle("Hello! Whats up")
                        listen_question = 1
                    question_answered = 1
                    if "what" in rec.PartialResult() and "oldest" in rec.PartialResult() and "sta" in rec.PartialResult() and "brazil" in rec.PartialResult():
                        text_to_speech_pyttsx3.runSoundFIle("Pernambuco")
                        question_answered = 0
                        listen_question = 0
                    elif "what" in rec.PartialResult() and "newest" in rec.PartialResult() and "sta" in rec.PartialResult() and "brazil" in rec.PartialResult():
                        text_to_speech_pyttsx3.runSoundFIle("Tocantins")
                        question_answered = 0
                        listen_question = 0
                    
                print(rec.PartialResult())
                #print(rec.Result())
            if dump_fn is not None:
                dump_fn.write(data)

except KeyboardInterrupt:
    print("\nDone")
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ": " + str(e))
