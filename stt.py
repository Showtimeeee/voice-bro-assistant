import vosk
import json
import pyaudio
import config


class SpeechToText:
    def __init__(self):
        self.model = vosk.Model(config.VOSK_MODEL_PATH)
        self.CHUNK = 4000
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000

    def listen(self):
        rec = vosk.KaldiRecognizer(self.model, self.RATE)
        p = pyaudio.PyAudio()
        stream = p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
        )

        try:
            while True:
                data = stream.read(self.CHUNK, exception_on_overflow=False)
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get("text", "")
                    if text:
                        return text
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
