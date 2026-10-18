# A smart way to calculate the hitbox is to divide a larger hitbox
# into smaller hitboxes based on the length of each word
def get_words(line: str) -> list:
    if not line or line.strip() == "":
        return []
        
    words = line.split()
    total_word_length = 0
    for word in words:
        total_word_length += len(word)
    
    results = [] 
    current_percentage_start = 0.0
    
    if total_word_length == 0:
        return []

    for word in words:
        procent = (len(word) / total_word_length) * 100
        
        procent_end = current_percentage_start + procent

        results.append({
            "word": word,
            "procent_start": round(current_percentage_start, 2),
            "procent_end": round(procent_end, 2)
        })
        
        current_percentage_start = procent_end

    return results