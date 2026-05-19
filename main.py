from tts import TextToSpeech
from stt import SpeechToText
from commands import CommandProcessor


def main():
    tts = TextToSpeech()
    stt = SpeechToText()
    commands = CommandProcessor()

    print("Голосовой помощник запущен. Скажите 'бро' для активации.")

    try:
        while True:
            stt.wait_for_wake_word("бро")
            print("Слушаю команду...")

            user_input = stt.listen()
            if not user_input:
                continue

            print(f"Вы сказали: {user_input}")
            response = commands.process(user_input)
            print(f"Ответ: {response}")

            tts.speak(response)

    except KeyboardInterrupt:
        print("\nЗавершение работы...")
    finally:
        stt.close()


if __name__ == "__main__":
    main()
