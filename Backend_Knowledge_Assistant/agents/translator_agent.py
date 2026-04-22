from langdetect import detect

def translate_to_english(text: str) -> str:
    """
    Placeholder translation logic.
    Replace with real API (Azure / OpenAI / DeepL) if needed.
    """
    return text  # stub for now


def translate_if_needed(query: str) -> str:
    try:
        lang = detect(query)
        if lang != "en":
            return translate_to_english(query)
    except Exception:
        pass

    return query