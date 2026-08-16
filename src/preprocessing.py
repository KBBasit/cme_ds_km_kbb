from langdetect import detect
from deep_translator import GoogleTranslator



def translate_text_to_english(text_list):
    """
    Translates the given text to English using Google Translator. Checks 
    the language of each text string and translates only if it is not already
    in English.
    Args:
        text_list (list): List of text strings to be translated into English.
    Returns:
        list: A list of translated text strings in English.
    """
    translated_text_list = []
    for i in text_list:
        if detect(i) == "en":
            translated_text_list.append(i)
        else:
            translated_text = GoogleTranslator(source='auto', target='en').translate(i)
            translated_text_list.append(translated_text)

    return translated_text_list