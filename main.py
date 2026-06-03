import os
import time
import shutil
from assistant.log import setup_logging, logger
from assistant.tts import TextToSpeech
from assistant.stt import SpeechToText
from assistant.commands import CommandProcessor
from assistant.vad import VoiceActivityDetector


_VAD_FRAME = None

def _check_dependencies():
    warnings = []

    from assistant.config import VOSK_MODEL_PATH, API_KEYS
    if not os.path.isdir(VOSK_MODEL_PATH):
        warnings.append(
            f"Vosk-модель не найдена: {VOSK_MODEL_PATH}"
        )

    if not shutil.which("ffplay"):
        warnings.append("ffplay не найден. Музыка не будет работать.")

    if not API_KEYS["weather"]:
        warnings.append(
            "OPENWEATHERMAP_KEY не задан. Погода недоступна."
        )
    if not API_KEYS["news"]:
        warnings.append("NEWSAPI_KEY не задан. Новости недоступны.")

    return warnings


def _get_vad_frame(rate: int) -> int:
    global _VAD_FRAME
    if _VAD_FRAME is None:
        _VAD_FRAME = int(rate * 0.03)
    return _VAD_FRAME


def _wait_for_speech_or_end(tts, stt, vad):
    """Monitor mic while TTS speaks. Return True if user interrupted."""
    frame = _get_vad_frame(stt.RATE)
    while tts.is_speaking():
        data = stt.stream.read(frame, exception_on_overflow=False)
        if vad.is_speech(data, stt.RATE):
            tts.stop()
            return True
        time.sleep(0.001)
    return False


def _handle_command(stt, tts, commands, vad, source="бро"):
    user_input = stt.listen()
    if not user_input:
        return False
    logger.info(f"Команда ({source}): {user_input}")
    response = commands.process(user_input)
    logger.info(f"Ответ: {response}")
    tts.speak(response)
    return _wait_for_speech_or_end(tts, stt, vad)


def main():
    setup_logging()
    logger.info("Голосовой помощник запущен")

    for w in _check_dependencies():
        logger.warning(w)
        print(f"  ⚠ {w}")

    tts = TextToSpeech()
    stt = SpeechToText()
    vad = VoiceActivityDetector()
    commands = CommandProcessor(
        reminder_callback=lambda text: tts.speak(f"Напоминание: {text}"),
        tts=tts,
    )

    print("Скажите 'бро' для активации.")
    commands.reminders.start()

    try:
        while True:
            stt.wait_for_wake_word("бро")
            while _handle_command(stt, tts, commands, vad, "бро"):
                pass

    except KeyboardInterrupt:
        logger.info("Завершение работы по запросу пользователя")
    except Exception as e:
        logger.exception("Необработанная ошибка")
    finally:
        commands.reminders.stop()
        stt.close()
        logger.info("Приложение остановлено")


if __name__ == "__main__":
    main()
