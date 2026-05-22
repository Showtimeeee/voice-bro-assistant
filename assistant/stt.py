import vosk
import json
import pyaudio
from . import config


class SpeechToText:
    def __init__(self):
        self.model = vosk.Model(config.VOSK_MODEL_PATH)
        self.CHUNK = 4000
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
        )

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def wait_for_wake_word(self, wake_word="бро"):
        rec = vosk.KaldiRecognizer(self.model, self.RATE)
        rec.SetKeywords([wake_word])

        while True:
            data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            if rec.AcceptWaveform(data):
                return

    def listen(self):
        rec = vosk.KaldiRecognizer(self.model, self.RATE)

        while True:
            data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if text:
                    return text
