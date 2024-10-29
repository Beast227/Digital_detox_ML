import joblib
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import LabelEncoder

# Initialize the vectorizer, classifier, and label encoder
vectorizer = TfidfVectorizer()
classifier = SGDClassifier()
label_encoder = LabelEncoder()

# Load the initial data (if any) to fit the vectorizer and label encoder
# This should be your initial training data
initial_inputs = ["initial sample 1", "initial sample 2"]
initial_labels = ["class1", "class2"]
all_classes = ["class1", "class2", "class3", "class4", "class5", "class6", "class7"]

# Fit the vectorizer and label encoder on the initial data
X_initial = vectorizer.fit_transform(initial_inputs)
y_initial = label_encoder.fit_transform(initial_labels)
label_encoder.fit(all_classes)

# Initial partial fit with all classes specified
classifier.partial_fit(X_initial, y_initial, classes=np.arange(len(all_classes)))

# Connect to the database and retrieve feedback
conn = sqlite3.connect('feedback.db')
cursor = conn.cursor()
cursor.execute('SELECT input_text, true_label FROM feedback')
rows = cursor.fetchall()
conn.close()

# Prepare the data for retraining
inputs = [row[0] for row in rows]
labels = [row[1] for row in rows]

# Vectorize the inputs and encode the labels
X_feedback = vectorizer.transform(inputs)
y_feedback = label_encoder.transform(labels)

# Retrain the classifier with the feedback data
classifier.partial_fit(X_feedback, y_feedback)

# Save the retrained model
joblib.dump(classifier, 'model/classifier.pkl')
joblib.dump(vectorizer, 'model/vectorizer.pkl')
joblib.dump(label_encoder, 'model/label_encoder.pkl')

print("Model retrained with feedback data.")
