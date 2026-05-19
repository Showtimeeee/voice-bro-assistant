import pyttsx3
import threading


class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self._lock = threading.Lock()
        self.setup_voice()

    def setup_voice(self):
        voices = self.engine.getProperty("voices")
        if len(voices) > 1:
            self.engine.setProperty("voice", voices[1].id)
        self.engine.setProperty("rate", 150)

    def _speak(self, text):
        with self._lock:
            self.engine.say(text)
            self.engine.runAndWait()

    def speak(self, text):
        thread = threading.Thread(target=self._speak, args=(text,), daemon=True)
        thread.start()
        return thread
