import sqlite3

DATABASE_NAME = 'vocabulary.db'

def initialize_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hovered_words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL,
            translation TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# function to add a word and its translation to the database
def log_word(word: str, translation: str):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT COUNT(id) FROM hovered_words WHERE word = ?
    ''', (word,))

    count = cursor.fetchone()[0]

    if count != 0:
        conn.close()
        return

    cursor.execute('''
        INSERT INTO hovered_words (word, translation)
        VALUES (?, ?)
    ''', (word, translation))
    
    conn.commit()
    conn.close()

# function to retrieve all logged words from the database
def get_logged_words():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            word, 
            translation 
        FROM 
            hovered_words
        ORDER BY 
            timestamp DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    
    words_list = []
    for row in rows:
        words_list.append({
            'word': row[0],
            'definition': row[1],
            'count': 1
        })
    return words_list