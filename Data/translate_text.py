from deep_translator import GoogleTranslator

def translate_text(text):
    dest_language='ro'
    try:
        translated = GoogleTranslator(source='en', target=dest_language).translate(text)
        
        if translated:
            return translated
        else:
            return ""
            
    except Exception as e:
        return f"Eroare de traducere: {e}"