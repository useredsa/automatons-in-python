#!/usr/bin/python3
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
