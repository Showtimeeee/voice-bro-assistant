import pyttsx3

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.setup_voice()
        
    def setup_voice(self):
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  # Русский голос
        self.engine.setProperty('rate', 150)  # Скорость речи
        
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
