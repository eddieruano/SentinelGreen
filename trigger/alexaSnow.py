import snowboydecoder
import sys
import os
import signal
import RPi.GPIO as GPIO
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import Alexa as Alexa

interrupted = False

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)

model = sys.argv[1]

signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.6)
print('Listening... Press Ctrl+C to exit')
Alexa = Alexa.Alexa(21)
detector.start(detected_callback=Alexa.blink,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()