import pyttsx3
import threading


class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self._thread = None
        self.setup_voice()

    def setup_voice(self):
        voices = self.engine.getProperty("voices")
        if len(voices) > 1:
            self.engine.setProperty("voice", voices[1].id)
        self.engine.setProperty("rate", 150)

    def _speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def speak(self, text):
        self._thread = threading.Thread(target=self._speak, args=(text,), daemon=True)
        self._thread.start()
        return self._thread

    def is_speaking(self):
        return self._thread is not None and self._thread.is_alive()

    def get_rate(self):
        return self.engine.getProperty("rate")

    def set_rate(self, value):
        self.engine.setProperty("rate", max(50, min(400, int(value))))

    def get_voices(self):
        return self.engine.getProperty("voices")

    def set_voice(self, index):
        voices = self.get_voices()
        if 0 <= index < len(voices):
            self.engine.setProperty("voice", voices[index].id)

    def get_volume(self):
        return self.engine.getProperty("volume")

    def set_volume(self, value):
        self.engine.setProperty("volume", max(0.0, min(1.0, float(value))))

    def stop(self):
        self.engine.stop()
