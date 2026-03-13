import vosk
import wave
import json
import config

class SpeechToText:
    def __init__(self):
        self.model = vosk.Model(config.VOSK_MODEL_PATH)
        self.rec = vosk.Recognizer()
        
    def listen(self):
        with wave.open("input.wav", "rb") as wf:
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
                raise ValueError("Неверный формат аудио")
                
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if self.rec.AcceptWaveform(data):
                    result = json.loads(self.rec.Result())
                    if result['text']:
                        return result['text']
            result = json.loads(self.rec.FinalResult())
            return result['text']
