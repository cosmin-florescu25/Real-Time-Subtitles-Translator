import requests
import re
from translate_text import translate_text
def clean_text(word: str) -> str:
    if not word:
        return ""
    
    cleaned_word = re.sub(r'[^a-zA-Z]', '', word)
    
    cleaned_word = cleaned_word.lower()

    return cleaned_word.strip()

def get_example_sentence(word1: str) -> str:
    word = clean_text(word1)
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    r = requests.get(url).json()

    if isinstance(r, dict) and r.get("title") == "No Definitions Found":
        return "Nu e gasit in dictionar."

    res = translate_text(r[0]["meanings"][0]["definitions"][0]["definition"])

    return res
    
if __name__ == "__main__":
    test_word = "example"
    definition = get_example_sentence(test_word)
    print(f"Definition for '{test_word}': {definition}")