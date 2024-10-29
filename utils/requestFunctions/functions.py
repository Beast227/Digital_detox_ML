import sqlite3

# Initialize the database
def init_db():
    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT,
            true_label TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_feedback(input_text, true_label):
    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO feedback (input_text, true_label)
        VALUES (?, ?)
    ''', (input_text, true_label))
    conn.commit()
    conn.close()