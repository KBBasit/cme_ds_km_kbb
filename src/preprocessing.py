from googletrans import Translator



async def translate_text(text):
    """
    Translates the given text to English using the googletrans library.
    Args:
        text (str): The text to be translated.

    Returns:
        str: The translated text in English.
    """
    translator = Translator()
    translation = await translator.translate(text, dest='en')

    return translation.text