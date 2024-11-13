import sqlite3
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import joblib

# Function to initialize the database (if not already initialized)
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

# Function to save new feedback
def save_feedback(input_text, true_label):
    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO feedback (input_text, true_label)
        VALUES (?, ?)
    ''', (input_text, true_label))
    conn.commit()
    conn.close()

# Function to extract feedback data from the database
def extract_feedback():
    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()
    cursor.execute('SELECT input_text, true_label FROM feedback')
    rows = cursor.fetchall()
    conn.close()

    # Convert to a DataFrame
    feedback_df = pd.DataFrame(rows, columns=['detox_priorities', 'true_label'])
    return feedback_df

# Function to combine feedback data with the existing dataset
def get_combined_data(existing_data_path):
    # Load the existing dataset
    data = pd.read_csv(existing_data_path)

    # Extract feedback data from the database
    feedback_data = extract_feedback()

    # Combine the two datasets
    combined_data = pd.concat([data, feedback_data], ignore_index=True)
    return combined_data

# Function to retrain the KMeans model
def retrain_model(combined_data):
    # Preprocess the combined data
    # OneHotEncoding for categorical features
    categorical_features = [
        'screen_time', 'main_activity', 'social_media_time',
        'screen_time_challenges', 'detox_support', 'tech_free_breaks'
    ]
    encoder = OneHotEncoder()
    encoded_features = encoder.fit_transform(combined_data[categorical_features]).toarray()

    # TF-IDF Vectorizer for text data
    text_feature = combined_data['detox_priorities']
    vectorizer = TfidfVectorizer(max_features=100)
    text_features = vectorizer.fit_transform(text_feature).toarray()

    # Combine features
    features = np.hstack((encoded_features, text_features))

    # Retrain the KMeans model
    num_clusters = 6  # You can adjust the number of clusters as needed
    kmeans = KMeans(n_clusters=num_clusters, n_init=10, random_state=42)
    combined_data['Cluster'] = kmeans.fit_predict(features)

    # Save the updated model and encoders for future use
    joblib.dump(kmeans, 'kmeans_model.pkl')
    joblib.dump(encoder, 'encoder.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')

    print("Model retrained and saved successfully!")

# Example usage
if __name__ == "__main__":
    # Initialize the database (if not already initialized)
    init_db()

    # Path to the existing data CSV
    existing_data_path = "path_to_your_existing_dataset.csv"

    # Combine feedback data with the existing dataset and retrain the model
    combined_data = get_combined_data(existing_data_path)
    retrain_model(combined_data)
