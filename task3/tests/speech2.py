#!/usr/bin/python3
import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print('Un momento de silencio para medir el nivel de ruido ambiente')
    r.adjust_for_ambient_noise(source)
    print("Limite de silencio: %f" % r.energy_threshold)
    f = open('salida.wav','wb')
    while True:
        try:
            print('Capturando...')
            # Capturar el audio
            audio = r.listen(source,timeout=1)
            print('¡Tengo audio!')
            f.write(audio.get_wav_data())
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
            print('Timeout')
