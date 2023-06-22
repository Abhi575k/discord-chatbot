import re
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def remove_punctuation(text):
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Return preprocessed text
    return text

def load_model():
    filename = os.getenv('MODEL_LATEST')
    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model

def preprocess_text(data):
    df = pd.read_csv(os.getenv('INPUT_DATA'))
    data = pd.DataFrame({'Input':[data]})
    data = data._append(df, ignore_index=True)

    data['Input'] = data['Input'].apply(remove_punctuation)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(data['Input'])
    return X

def predict_data(data):
    data = preprocess_text(data)
    svm = load_model()
    y = svm.predict(data)
    
    return y[0]