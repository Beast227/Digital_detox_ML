import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK data files
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')

# Initialize the lemmatizer and stop words
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    # Lowercasing
    text = text.lower()
    
    # Removing punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenization
    tokens = nltk.word_tokenize(text)
    
    # Removing stop words and lemmatization
    processed_tokens = [
        lemmatizer.lemmatize(token) for token in tokens if token not in stop_words
    ]
    
    # Joining tokens back into a single string
    return ' '.join(processed_tokens)

def preprocess_input(data):
    processed_data = {}
    for key, value in data["input"].items():
        processed_data[key] = preprocess_text(value)
    return processed_data