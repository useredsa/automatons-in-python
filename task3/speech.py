#!/usr/bin/python3
import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print('¡Habla ahora o calla para siempre!')
    while True:
        try:
            # Capturar el audio
            audio = r.listen(source,timeout=1)
            # Reconocer el audio
            try:
                salida = r.recognize_google(audio,language="es-ES")
                if salida == 'fin':
                    break
                else:
                    print(salida)
            except sr.UnknownValueError:
                print("Google Speech Recognition no comprende")
            except sr.RequestError as e:
                print("Error conectado a Google Speech Recognition")
        except sr.WaitTimeoutError:
            pass
print('Fin')
