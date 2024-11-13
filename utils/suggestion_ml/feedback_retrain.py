def extract_feedback():
    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()
    cursor.execute('SELECT input_text, user_cluster, feedback FROM feedback')
    feedback_data = cursor.fetchall()
    conn.close()
    
    # Convert to DataFrame for processing
    feedback_df = pd.DataFrame(feedback_data, columns=['detox_priorities', 'Cluster', 'feedback'])
    return feedback_df

# Retrain with existing and feedback data combined
def retrain_model():
    # Load initial dataset
    data = load_data()

    # Extract feedback and combine
    feedback_data = extract_feedback()
    combined_data = pd.concat([data, feedback_data], ignore_index=True)

    # Preprocess and retrain model
    features, encoder, vectorizer = preprocess_data(combined_data)
    kmeans, clusters = train_clustering_model(features)
    combined_data['Cluster'] = clusters  # Update clusters in data

    # Save the updated model
    save_model(kmeans, encoder, vectorizer)
    print("Model retrained with feedback data!")


def update_suggestions_pool(cluster, feedback):
    if cluster in suggestions_pool:
        if feedback not in suggestions_pool[cluster]:
            suggestions_pool[cluster].append(feedback)
    else:
        suggestions_pool[cluster] = [feedback]
