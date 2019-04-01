import pyttsx3
engine = pyttsx3.init()
rate = engine.getProperty('rate')
voices = engine.getProperty('voices')
engine.setProperty('voice', 'spanish')
engine.setProperty('rate', rate-20)
engine.say('Hola!')
engine.say('¿Qué ¡tal estas?')
engine.runAndWait()
