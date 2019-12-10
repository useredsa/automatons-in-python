#!/usr/bin/python3
<<<<<<< HEAD
import speech_recognition as sr
from TextFormatter  import TextFormatter

r = sr.Recognizer()
with sr.Microphone() as source:
    print('Un momento de silencio para medir el nivel de ruido ambiente')
    r.adjust_for_ambient_noise(source)
    print("Limite de silencio: %f" % r.energy_threshold)
    f = open('salida.wav', 'wb')

    textForm = TextFormatter(10)
    # Capturar el audio
    while True:
        try:
            print('Capturando...')
            audio = r.listen(source, timeout=1)
            print('Capté algo')
            f.write(audio.get_wav_data())
            # Reconocer el audio
            try:
                salida = r.recognize_google(audio, language="es-ES")
                if salida == 'fin':
                    break
                else:
                    textForm.processLine(salida, breakLine=False)
            except sr.UnknownValueError:
                print("Google Speech Recognition no comprende")
            except sr.RequestError as e:
                print("Error conectado a Google Speech Recognition")
        except sr.WaitTimeoutError:
            print('Timeout')
=======

'''TextFormatter interactor to process audio.'''

import speech_recognition as sr
import TextFormatter
import sys

with sr.Microphone() as source:
    r = sr.Recognizer()
    print('Gracias por usar voiceRecognition.')
    print('Pulsa [Enter] cuando estés listo para medir el nivel de ruido.')
    input()

    print('Un momento de silencio para medir el nivel de ruido ambiente')
    r.adjust_for_ambient_noise(source)
    print(f'Limite de silencio: {r.energy_threshold}')
    while True:
        print('Introduce el número de caracteres por línea para empezar:', end='')
        try:
            lineLen = int(input())
            txtForm = TextFormatter.SpanishFormatter(lineLen)
        except ValueError:
            print('Número de caracteres no válido.')
            continue
        break

    print()
    print('Ya puedes hablar. Di la palabra fin para terminar.')
    while True:
        try:
            print('[>]', end='')
            # Capturar el audio
            audio = r.listen(source,timeout=3)
            try:
                salida = r.recognize_google(audio,language="es-ES")
                if salida == 'fin':
                    break
                else:
                    txtForm.processLine(salida)
            except sr.UnknownValueError:
                print("Google Speech Recognition no comprende", file=sys.stderr)
            except sr.RequestError as e:
                print("Error conectado a Google Speech Recognition", file=sys.stderr)
        except sr.WaitTimeoutError:
            print('Timeout', file=sys.stderr)
    print()
>>>>>>> 4b77ade17c903c4ecd49c6ceaf10e020ab38f462
