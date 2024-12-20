import sqlite3
import pandas as pd

# Database initialization
def init_db():
    conn = sqlite3.connect('survey_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS survey_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            screen_time TEXT,
            main_activity TEXT,
            social_media_time TEXT,
            reduce_social_media TEXT,
            work_screen_time TEXT,
            tech_free_breaks TEXT,
            detox_goal TEXT,
            screen_time_challenges TEXT,
            detox_support TEXT,
            detox_priorities TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Save new user data to the database
def save_survey_to_db(new_user_data):
    conn = sqlite3.connect('survey_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO survey_data (
            screen_time, main_activity, social_media_time, reduce_social_media, work_screen_time, 
            tech_free_breaks, detox_goal, screen_time_challenges, detox_support, detox_priorities
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        new_user_data['screen_time'],
        new_user_data['main_activity'],
        new_user_data['social_media_time'],
        new_user_data['reduce_social_media'],
        new_user_data['work_screen_time'],
        new_user_data['tech_free_breaks'],
        new_user_data['detox_goal'],
        new_user_data['screen_time_challenges'],
        new_user_data['detox_support'],
        new_user_data['detox_priorities']
    ))
    conn.commit()
    conn.close()

# Populate database from CSV file
def populate_db_from_csv(csv_file_path):
    # Load data from CSV
    df = pd.read_csv(csv_file_path)
    
    # Iterate over each row and insert it into the database
    for _, row in df.iterrows():
        new_user_data = {
            'screen_time': row['screen_time'],
            'main_activity': row['main_activity'],
            'social_media_time': row['social_media_time'],
            'reduce_social_media': row['reduce_social_media'],
            'work_screen_time': row['work_screen_time'],
            'tech_free_breaks': row['tech_free_breaks'],
            'detox_goal': row['detox_goal'],
            'screen_time_challenges': row['screen_time_challenges'],
            'detox_support': row['detox_support'],
            'detox_priorities': row['detox_priorities']
        }
        save_survey_to_db(new_user_data)

# Check the number of records in the database
def get_record_count():
    conn = sqlite3.connect('survey_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM survey_data")
    count = cursor.fetchone()[0]
    conn.close()
    return count
