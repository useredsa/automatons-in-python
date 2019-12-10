#!/usr/bin/python3

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
