import re
import string
import unittest
from pathlib import Path

from translations import CONTEXTUAL_HELP, TRANSLATIONS


SUPPORTED_LANGUAGES = ("en", "lt", "no", "es", "de", "fr")


def _placeholders(value: str) -> set[str]:
    return {
        field_name
        for _, field_name, _, _ in string.Formatter().parse(str(value))
        if field_name
    }


class TranslationCoverageTests(unittest.TestCase):
    def test_all_supported_languages_have_every_english_key(self):
        english_keys = set(TRANSLATIONS["en"])
        for language in SUPPORTED_LANGUAGES:
            with self.subTest(language=language):
                self.assertEqual(set(TRANSLATIONS[language]), english_keys)

    def test_translations_preserve_format_placeholders(self):
        english = TRANSLATIONS["en"]
        for language in SUPPORTED_LANGUAGES:
            for key, expected in english.items():
                with self.subTest(language=language, key=key):
                    self.assertEqual(
                        _placeholders(TRANSLATIONS[language][key]),
                        _placeholders(expected),
                    )

    def test_contextual_help_is_complete_for_every_language(self):
        english_help_keys = set(CONTEXTUAL_HELP["en"])
        for language in SUPPORTED_LANGUAGES:
            with self.subTest(language=language):
                self.assertEqual(set(CONTEXTUAL_HELP[language]), english_help_keys)

    def test_app_translation_calls_exist_in_english_baseline(self):
        app_source = Path("app.py").read_text(encoding="utf-8")
        literal_keys = set(re.findall(r"""\bt\(["']([^"']+)["']""", app_source))
        missing = {
            key for key in literal_keys
            if "{" not in key and key not in TRANSLATIONS["en"]
        }
        self.assertEqual(missing, set())


if __name__ == "__main__":
    unittest.main()
