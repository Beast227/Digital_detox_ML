import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import joblib
import sqlite3
from . import Db_functions

# Global variables for file paths
MODEL_PATH = 'model2/kmeans_model.pkl'
ENCODER_PATH = 'model2/encoder.pkl'
VECTORIZER_PATH = 'model2/vectorizer.pkl'
DB_PATH = 'survey_data.db'

# Load survey data from the database
def load_data():
    conn = sqlite3.connect(DB_PATH)
    data = pd.read_sql_query('SELECT * FROM survey_data', conn)
    conn.close()
    return data

# Helper function to preprocess data (both training and new user data)
def preprocess_data(data, encoder=None, vectorizer=None, fit=False):
    categorical_features = [
        'screen_time', 'main_activity', 'social_media_time', 
        'reduce_social_media', 'work_screen_time', 'tech_free_breaks', 
        'detox_goal', 'screen_time_challenges', 'detox_support'
    ]

    # Encode categorical features
    if fit:
        encoder = OneHotEncoder()
        encoded_features = encoder.fit_transform(data[categorical_features]).toarray()
    else:
        encoded_features = encoder.transform(data[categorical_features]).toarray()

    # TF-IDF vectorization for text features
    text_feature = data['detox_priorities']
    if fit:
        vectorizer = TfidfVectorizer(max_features=100)
        text_features = vectorizer.fit_transform(text_feature).toarray()
    else:
        text_features = vectorizer.transform(text_feature).toarray()

    # Combine encoded categorical and text features
    features = np.hstack((encoded_features, text_features))
    return features, encoder, vectorizer

# Train and save the clustering model
def train_clustering_model(features, n_clusters=5):
    kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
    kmeans.fit(features)
    return kmeans

# Save models and encoders
def save_model_objects(model, encoder, vectorizer):
    joblib.dump(model, MODEL_PATH)
    joblib.dump(encoder, ENCODER_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

# Build and train the model pipeline
def build_and_train_model():
    data = load_data()
    features, encoder, vectorizer = preprocess_data(data, fit=True)
    kmeans = train_clustering_model(features)
    save_model_objects(kmeans, encoder, vectorizer)
    data['Cluster'] = kmeans.predict(features)  # Assign clusters to data
    return data, kmeans, encoder, vectorizer

# Load model and encoders
def load_model_objects():
    kmeans = joblib.load(MODEL_PATH)
    encoder = joblib.load(ENCODER_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    return kmeans, encoder, vectorizer

# Predict cluster for a new user
def predict_user_cluster(new_user_data):
    # Save new user data to the database
    Db_functions.save_survey_to_db(new_user_data)

    # Load model and encoders if not loaded
    kmeans, encoder, vectorizer = load_model_objects()

    # Convert new user data to DataFrame for consistency
    new_user_df = pd.DataFrame([new_user_data])

    # Preprocess new user data
    features, _, _ = preprocess_data(new_user_df, encoder=encoder, vectorizer=vectorizer, fit=False)

    # Predict the cluster
    user_cluster = kmeans.predict(features)[0]
    return user_cluster

# # Example usage:
# if __name__ == "__main__":
#     # Uncomment the next line to build and train the model for the first time
#     # data, kmeans, encoder, vectorizer = build_and_train_model()

#     # New user data for prediction (example data)
#     new_user_data = {
#         'screen_time': '2-4 hours',
#         'main_activity': 'Reading',
#         'social_media_time': '1-2 hours',
#         'reduce_social_media': 'Disable notifications',
#         'work_screen_time': '2-4 hours',
#         'tech_free_breaks': 'Yes',
#         'detox_goal': 'Improve focus and productivity',
#         'screen_time_challenges': 'Reducing distractions',
#         'detox_support': 'Family',
#         'detox_priorities': 'Improve focus and productivity'
#     }

#     # Predict the cluster for the new user
#     user_cluster = predict_user_cluster(new_user_data)
#     print(f"The predicted cluster for the new user is: {user_cluster}")