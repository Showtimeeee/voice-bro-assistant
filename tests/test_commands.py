import pytest
from assistant.commands import CommandProcessor


@pytest.fixture
def processor():
    return CommandProcessor()


def test_greeting(processor):
    result = processor.process("привет")
    assert isinstance(result, str)
    assert len(result) > 3


def test_greeting_case_insensitive(processor):
    result = processor.process("ПРИВЕТ")
    assert isinstance(result, str)


def test_farewell(processor):
    result = processor.process("пока")
    assert isinstance(result, str)


def test_time(processor):
    result = processor.process("который час")
    assert "Сейчас" in result


def test_weather(processor):
    result = processor.process("какая погода")
    assert isinstance(result, str)


def test_news(processor):
    result = processor.process("новости")
    assert isinstance(result, str)


def test_calculator(processor):
    result = processor.process("посчитай 2+3")
    assert "Результат: 5" in result


def test_joke(processor):
    result = processor.process("расскажи шутку")
    assert isinstance(result, str)
    assert len(result) > 10


def test_help(processor):
    result = processor.process("помощь")
    assert "могу помочь" in result


def test_how_are_you(processor):
    result = processor.process("как дела")
    assert isinstance(result, str)


def test_search(processor):
    result = processor.process("найди python")
    assert isinstance(result, str)


def test_translate(processor):
    result = processor.process("переведи hello")
    assert "Перевод" in result


def test_note(processor):
    result = processor.process("запиши купить хлеб")
    assert "добавлена" in result


def test_show_notes(processor):
    result = processor.process("покажи заметки")
    assert isinstance(result, str)


def test_reminder(processor):
    result = processor.process("напомни позвонить")
    assert "сохранено" in result or "установлено" in result

def test_timed_reminder(processor):
    result = processor.process("напомни через 10 минут выключить чайник")
    assert "установлено" in result


def test_music(processor, mocker):
    mock_popen = mocker.patch("subprocess.Popen")
    mock_proc = mocker.Mock()
    mock_proc.poll.return_value = None
    mock_popen.return_value = mock_proc

    result = processor.process("включи Imagine Dragons")
    assert "Воспроизвожу" in result
    assert "Test Song" in result

def test_stop_music(processor, mocker):
    mocker.patch("subprocess.Popen")
    mock_proc = mocker.Mock()
    mock_proc.poll.return_value = None
    mocker.patch("subprocess.Popen", return_value=mock_proc)

    processor.process("включи Imagine Dragons")
    result = processor.process("выключи музыку")
    assert "остановлена" in result

def test_music_no_query(processor):
    result = processor.process("включи музыку")
    assert "Что включить" in result


def test_speed_faster(processor, mocker):
    mock_tts = mocker.Mock()
    mock_tts.get_rate.return_value = 150
    processor.tts = mock_tts
    result = processor.process("говори быстрее")
    assert "Скорость речи: 160" in result
    mock_tts.set_rate.assert_called_with(160)

def test_speed_slower(processor, mocker):
    mock_tts = mocker.Mock()
    mock_tts.get_rate.return_value = 150
    processor.tts = mock_tts
    result = processor.process("говори медленнее")
    assert "Скорость речи: 140" in result
    mock_tts.set_rate.assert_called_with(140)

def test_speed_normal(processor, mocker):
    mock_tts = mocker.Mock()
    processor.tts = mock_tts
    result = processor.process("нормальная скорость")
    assert "Скорость речи: 150" in result
    mock_tts.set_rate.assert_called_with(150)

def test_speed_set_number(processor, mocker):
    mock_tts = mocker.Mock()
    processor.tts = mock_tts
    result = processor.process("скорость речи 200")
    assert "Скорость речи: 200" in result
    mock_tts.set_rate.assert_called_with(200)

def test_speed_no_tts(processor):
    processor.tts = None
    result = processor.process("говори быстрее")
    assert "Ошибка" in result

def test_weather_no_key(processor):
    processor.weather_api_key = None
    result = processor.process("погода")
    assert "не настроен" in result

def test_weather_api_error(processor, mocker):
    mock_resp = mocker.Mock()
    mock_resp.status_code = 401
    mock_resp.json.return_value = {"message": "Invalid API key"}
    mocker.patch("requests.get", return_value=mock_resp)
    result = processor.process("погода")
    assert "Ошибка погоды" in result
    assert "401" in result
    assert "Invalid API key" in result

def test_news_no_key(processor):
    processor.news_api_key = None
    result = processor.process("новости")
    assert "не настроен" in result

def test_news_api_error(processor, mocker):
    mock_resp = mocker.Mock()
    mock_resp.status_code = 401
    mock_resp.json.return_value = {"message": "API key invalid"}
    mocker.patch("requests.get", return_value=mock_resp)
    result = processor.process("новости")
    assert "Ошибка новостей" in result
    assert "401" in result
    processor.tts = None
    result = processor.process("говори быстрее")
    assert "Ошибка" in result


def test_unknown_command(processor):
    result = processor.process("фывапролд")
    assert "Не совсем поняла" in result


def test_voice_male(processor, mocker):
    mock_tts = mocker.Mock()
    mock_tts.get_voices.return_value = [mocker.Mock(), mocker.Mock()]
    processor.tts = mock_tts
    result = processor.process("голос мужской")
    assert "изменён" in result
    mock_tts.set_voice.assert_called_with(0)

def test_voice_female(processor, mocker):
    mock_tts = mocker.Mock()
    mock_tts.get_voices.return_value = [mocker.Mock(), mocker.Mock()]
    processor.tts = mock_tts
    result = processor.process("голос женский")
    assert "изменён" in result
    mock_tts.set_voice.assert_called_with(1)

def test_volume_louder(processor, mocker):
    mock_tts = mocker.Mock()
    mock_tts.get_volume.return_value = 0.5
    processor.tts = mock_tts
    result = processor.process("громче")
    assert "Громкость: 60%" in result
    mock_tts.set_volume.assert_called_with(0.6)

def test_volume_quieter(processor, mocker):
    mock_tts = mocker.Mock()
    mock_tts.get_volume.return_value = 0.5
    processor.tts = mock_tts
    result = processor.process("тише")
    assert "Громкость: 40%" in result
    mock_tts.set_volume.assert_called_with(0.4)

def test_volume_set_number(processor, mocker):
    mock_tts = mocker.Mock()
    processor.tts = mock_tts
    result = processor.process("громкость 80")
    assert "Громкость: 80%" in result
    mock_tts.set_volume.assert_called_with(0.8)

def test_volume_no_tts(processor):
    processor.tts = None
    result = processor.process("громче")
    assert "Ошибка" in result

def test_repeat_last(processor):
    processor.process("привет")
    result = processor.process("повтори")
    assert result == processor._last_response

def test_repeat_empty(processor):
    result = processor.process("повтори")
    assert "ещё ничего" in result

def test_voice_no_tts(processor):
    processor.tts = None
    result = processor.process("голос мужской")
    assert "Ошибка" in result


def test_empty_command(processor):
    result = processor.process("")
    assert "Не совсем поняла" in result
