from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import sqlite3
import utils.requestFunctions.functions as function
import utils.preprocessing.preprocess as preprocess

app = Flask(__name__)

# Configure CORS to allow specific origins
CORS(app, resources={r"/*": {"origins": ["https://digitaldetoxer.netlify.app", "http://localhost:3000"]}})

# Load the trained classifier, vectorizer, and label encoder
classifier = joblib.load('model/classifier.pkl')
vectorizer = joblib.load('model/vectorizer.pkl')
label_encoder = joblib.load('model/label_encoder.pkl')

function.init_db()

@app.route('/predict', methods=['POST'])
def predict():
    # Step 1: Receive and validate input data
    input_data = request.json.get('input', {})
    
    # Check if input_data is a dictionary
    if not isinstance(input_data, dict):
        return jsonify({"error": "Invalid input format: expected a dictionary"}), 400
    
    # Step 2: Preprocess each field in the input data
    try:
        # Preprocess each value and combine into a single string
        combined_text = ' '.join(preprocess.preprocess_text(str(value)) for value in input_data.values())
        
        # Step 3: Transform the combined text with the TF-IDF vectorizer
        x_tfidf = vectorizer.transform([combined_text])
        
        # Step 4: Predict using the model
        prediction = classifier.predict(x_tfidf)
        predicted_label = label_encoder.inverse_transform([prediction])[0]
        
        return jsonify({"prediction": predicted_label})
    
    except Exception as e:
        print("Error during transformation or prediction:", e)
        return jsonify({"error": "Error in prediction"}), 500

@app.route('/feedback', methods=['POST'])
def feedback():
    # Receive and validate input data
    data = request.json
    if 'input' not in data or 'true_label' not in data:
        return jsonify({'error': 'Input and true_label are required'}), 400
    
    input_data = data['input']  # Extract input data
    true_label = data['true_label']
    
    # Check if input_data is a dictionary and preprocess accordingly
    if isinstance(input_data, dict):
        # Preprocess each value and combine into a single string
        combined_text = ' '.join(preprocess.preprocess_text(str(value)) for value in input_data.values())
    else:
        # If input_data is already a string, process it directly
        combined_text = preprocess.preprocess_text(input_data)
    
    # Vectorize the combined text
    input_vectorized = vectorizer.transform([combined_text])
    
    # Encode the true label
    true_label_encoded = label_encoder.transform([true_label])
    
    # Update the model with the new data
    classifier.partial_fit(input_vectorized, true_label_encoded)
    
    # Save the updated model
    joblib.dump(classifier, 'model/classifier.pkl')
    
    # Save feedback to the database
    function.save_feedback(combined_text, true_label)
    
    return jsonify({'status': 'Model updated with new feedback'})

if __name__ == '__main__':
    app.run(debug=True)
