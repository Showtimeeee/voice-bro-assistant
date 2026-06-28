import os
import sys
import time
import shutil
import argparse

from assistant.log import setup_logging, logger
from assistant.commands import CommandProcessor


_VAD_FRAME = None


def _parse_args():
    parser = argparse.ArgumentParser(description="Голосовой ассистент Бро")
    parser.add_argument(
        "--text", "-t",
        action="store_true",
        help="Текстовый режим (без микрофона и голоса)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Подробное логирование",
    )
    parser.add_argument(
        "--no-wake",
        action="store_true",
        help="Слушать команды без wake word",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Путь к Vosk-модели",
    )
    return parser.parse_args()


def _check_dependencies():
    warnings = []

    from assistant.config import VOSK_MODEL_PATH, API_KEYS
    if not os.path.isdir(VOSK_MODEL_PATH):
        warnings.append(f"Vosk-модель не найдена: {VOSK_MODEL_PATH}")

    if not shutil.which("ffplay"):
        warnings.append("ffplay не найден. Музыка не будет работать.")

    if not API_KEYS["weather"]:
        warnings.append("OPENWEATHERMAP_KEY не задан. Погода недоступна.")
    if not API_KEYS["news"]:
        warnings.append("NEWSAPI_KEY не задан. Новости недоступны.")

    return warnings


def _voice_loop(commands):
    from assistant.tts import TextToSpeech
    from assistant.stt import SpeechToText
    from assistant.vad import VoiceActivityDetector

    tts = TextToSpeech()
    stt = SpeechToText()
    vad = VoiceActivityDetector()

    commands.tts = tts
    commands.reminders.callback = lambda text: tts.speak(f"Напоминание: {text}")
    commands.timer_service.callback = lambda text: tts.speak(f"Таймер: {text}")
    commands.reminders.start()
    commands.timer_service.start()

    print("Скажите 'бро' для активации.")

    try:
        while True:
            stt.wait_for_wake_word("бро")
            while True:
                user_input = stt.listen()
                if not user_input:
                    break
                logger.info(f"Команда: {user_input}")
                response = commands.process(user_input)
                logger.info(f"Ответ: {response}")
                tts.speak(response)

                frame = _get_vad_frame(stt.RATE)
                interrupted = False
                while tts.is_speaking():
                    data = stt.stream.read(frame, exception_on_overflow=False)
                    if vad.is_speech(data, stt.RATE):
                        tts.stop()
                        interrupted = True
                        break
                    time.sleep(0.001)
                if not interrupted:
                    break
    finally:
        commands.reminders.stop()
        commands.timer_service.stop()
        stt.close()


def _text_loop(commands):
    commands.reminders.callback = lambda text: print(f"⏰ Напоминание: {text}")
    commands.timer_service.callback = lambda text: print(f"⏱ Таймер: {text}")
    commands.reminders.start()
    commands.timer_service.start()
    print("Текстовый режим. Введите 'пока' для выхода.")
    print()

    try:
        while True:
            user_input = input("> ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("пока", "выход", "quit", "exit"):
                print("До свидания!")
                break
            logger.info(f"Команда: {user_input}")
            response = commands.process(user_input)
            print(response)
    finally:
        commands.reminders.stop()
        commands.timer_service.stop()


def _get_vad_frame(rate: int) -> int:
    global _VAD_FRAME
    if _VAD_FRAME is None:
        _VAD_FRAME = int(rate * 0.03)
    return _VAD_FRAME


def main():
    args = _parse_args()

    setup_logging(debug=args.debug)

    if args.model:
        from assistant.config import VOSK_MODEL_PATH
        import assistant.config as _cfg
        _cfg.VOSK_MODEL_PATH = args.model

    logger.info("Голосовой помощник запущен")

    for w in _check_dependencies():
        logger.warning(w)
        print(f"  ⚠ {w}")

    commands = CommandProcessor(
        reminder_callback=None,
        timer_callback=None,
        tts=None,
    )

    if args.text:
        _text_loop(commands)
    else:
        _voice_loop(commands)


if __name__ == "__main__":
    main()
