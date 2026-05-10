from langdetect import detect, LangDetectException
from deep_translator import GoogleTranslator


def detect_language(text: str, fallback: str = "en") -> str:
    if not text or not text.strip():
        return fallback
    try:
        return detect(text)
    except LangDetectException:
        return fallback


def translate_text(text: str, source_lang: str = "auto", target_lang: str = "en") -> str:
    if not text:
        return ""
    if source_lang == target_lang:
        return text
    try:
        return GoogleTranslator(source=source_lang, target=target_lang).translate(text)
    except Exception:
        return text


def to_english(text: str, source_lang: str = "auto") -> str:
    return translate_text(text=text, source_lang=source_lang, target_lang="en")


def from_english(text: str, target_lang: str = "en") -> str:
    return translate_text(text=text, source_lang="en", target_lang=target_lang)
