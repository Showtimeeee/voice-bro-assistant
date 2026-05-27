import sys
import types
import pytest
from pathlib import Path

# --- mock external modules before any assistant imports ---
_MOCK_MODULES = [
    'vosk', 'pyaudio', 'pyttsx3', 'dotenv',
    'PIL', 'PIL.Image', 'duckduckgo_search', 'duckduckgo_search.DDGS',
]
for name in _MOCK_MODULES:
    if name not in sys.modules:
        parts = name.split('.')
        parent = '.'.join(parts[:-1])
        if parent and parent not in sys.modules:
            sys.modules[parent] = types.ModuleType(parent)
        sys.modules[name] = types.ModuleType(name)

# mock requests properly
class _MockResponse:
    status_code = 200
    def json(self):
        return {'articles': []}

class _MockRequests:
    get = staticmethod(lambda *a, **kw: _MockResponse())
    class exceptions:
        RequestException = Exception

sys.modules['requests'] = _MockRequests()

# mock pytz
import datetime

class _MockTimezone(datetime.tzinfo):
    def localize(self, dt):
        return dt.replace(tzinfo=self)
    def utcoffset(self, dt):
        return datetime.timedelta(hours=3)
    def tzname(self, dt):
        return 'MSK'
    def dst(self, dt):
        return datetime.timedelta(0)
    def __str__(self):
        return 'Europe/Moscow'

class _MockPytz:
    timezone = staticmethod(lambda x: _MockTimezone())
    utc = datetime.timezone.utc

sys.modules['pytz'] = _MockPytz()

# mock dotenv.load_dotenv to do nothing
import dotenv
dotenv.load_dotenv = lambda *a, **kw: None

# set env vars for config
import os
os.environ['OPENWEATHERMAP_KEY'] = 'test_key'
os.environ['NEWSAPI_KEY'] = 'test_key'

# set BASE_DIR to project root so relative paths work
os.environ['NOTES_FILE'] = str(Path(__file__).parent / 'test_notes.txt')
os.environ['REMINDERS_FILE'] = str(Path(__file__).parent / 'test_reminders.txt')

# mock argostranslate
class _MockTranslator:
    def translate(self, text, from_code, to_code):
        return f"[{from_code}→{to_code}] {text}"
    def get_installed_languages(self):
        Lang = type('Lang', (), {'code': 'en'})
        return [Lang()]

class _MockPackage:
    def update_package_index(self):
        pass
    def get_available_packages(self):
        return []
    def install_from_path(self, path):
        pass

class _MockArgos:
    translate = _MockTranslator()
    package = _MockPackage()

sys.modules['argostranslate'] = _MockArgos()
sys.modules['argostranslate.package'] = _MockArgos.package
sys.modules['argostranslate.translate'] = _MockArgos.translate


@pytest.fixture(autouse=True)
def clean_test_files():
    yield
    for f in ['test_notes.txt', 'test_reminders.txt']:
        p = Path(__file__).parent / f
        if p.exists():
            p.unlink()
