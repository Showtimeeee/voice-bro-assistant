from tts import TextToSpeech
from stt import SpeechToText
from commands import CommandProcessor


def main():
    tts = TextToSpeech()
    stt = SpeechToText()
    commands = CommandProcessor()
    
    print("Голосовой помощник запущен")
    
    while True:
        try:
            user_input = stt.listen()
            print(f"Вы сказали: {user_input}")
            response = commands.process(user_input)
            tts.speak(response)
            
        except Exception as e:
            print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
