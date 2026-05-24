import argostranslate.package
import argostranslate.translate
from .log import logger

_LANG_NAMES = {
    "русский": "ru",
    "английский": "en",
    "французский": "fr",
    "немецкий": "de",
    "испанский": "es",
    "итальянский": "it",
    "португальский": "pt",
    "китайский": "zh",
    "японский": "ja",
    "корейский": "ko",
}

_DEFAULT_PAIRS = [("ru", "en"), ("en", "ru")]


class OfflineTranslator:
    def __init__(self):
        self._installed = False

    def _ensure_models(self):
        if self._installed:
            return
        if argostranslate.translate.get_installed_languages():
            self._installed = True
            return
        try:
            argostranslate.package.update_package_index()
            available = argostranslate.package.get_available_packages()
            for from_code, to_code in _DEFAULT_PAIRS:
                pkg = next(
                    (p for p in available if p.from_code == from_code and p.to_code == to_code),
                    None
                )
                if pkg:
                    logger.info(f"Загрузка модели {from_code}→{to_code}...")
                    argostranslate.package.install_from_path(pkg.download())
            self._installed = True
            logger.info("Модели перевода установлены")
        except Exception as e:
            logger.warning(f"Не удалось загрузить модели: {e}")

    def translate(self, text, to_lang="ru"):
        self._ensure_models()
        installed = argostranslate.translate.get_installed_languages()
        installed_codes = {l.code for l in installed}
        for from_code in installed_codes:
            if from_code == to_lang:
                continue
            try:
                result = argostranslate.translate.translate(text, from_code, to_lang)
                if result and result != text:
                    return result
            except Exception:
                continue
        return None

    def parse_command(self, command):
        text = command.replace("переведи", "").replace("перевод", "").strip()
        target = "ru"

        for name, code in _LANG_NAMES.items():
            if f"на {name}" in text or f"на{name}" in text:
                target = code
                text = text.replace(f"на {name}", "").replace(f"на{name}", "").replace(name, "").strip()
                break

        return text, target
