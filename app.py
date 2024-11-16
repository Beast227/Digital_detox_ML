from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import sqlite3
import utils.requestFunctions.functions as function
import utils.preprocessing.preprocess as preprocess
import utils.suggestion_ml.preProcessingAndClustering as suggestions_ml
import utils.suggestion_ml.predict_suggestions as predictSuggestions
import utils.suggestion_ml.Db_functions as db

app = Flask(__name__)

# Configure CORS to allow specific origins
CORS(app, resources={r"/*": {"origins": ["https://digitaldetoxer.netlify.app", "http://localhost:3000"]}})

# Load the trained classifier, vectorizer, and label encoder
classifier = joblib.load('model1/classifier.pkl')
vectorizer = joblib.load('model1/vectorizer.pkl')
label_encoder = joblib.load('model1/label_encoder.pkl')

function.init_db()
db.init_db()
record_count = db.get_record_count()
print(f"Number of records in the database: {record_count}")
suggestions_ml.build_and_train_model()

@app.route('/predict', methods=['POST'])
def predict():
    # Step 1: Receive and validate input data
    data = request.json
    input_data = data['input']
    
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

        suggestions = predictSuggestions.generate_suggestions(data['cluster'])
        
        return jsonify({
            "prediction": predicted_label, 
            "suggestions" : suggestions
            })
    
    except Exception as e:
        print("Error during transformation or prediction:", e)
        return jsonify({"error": "Error in prediction"}), 500

@app.route('/feedback', methods=['POST'])
def feedback():
    # Receive and validate input data
    data = request.json
    if 'feedback' not in data :
        return jsonify({"error": "Feedback data not sent"})
    
    predictSuggestions.collect_feedback(data['cluster'], data['feedback'])
    
    return jsonify({'status': 'Feedback is stored'})

@app.route('/cluster', methods=['POST'])
def cluster(): 
    data = request.json
    if 'input' not in data:
        return jsonify({'message': 'Input are required'}), 400
    
    cluster = suggestions_ml.predict_user_cluster(data['input'])

    return jsonify({'cluster': int(cluster)})

if __name__ == '__main__':
    app.run(debug=True)
