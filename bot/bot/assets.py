# Import libraries
import pandas as pd
import sklearn
from dagster import asset
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle
from datetime import datetime

import os

from dotenv import load_dotenv

load_dotenv()


@asset
def import_data():
    df = pd.read_csv(os.getenv('DATA'))
    return df

@asset
def filter_data(import_data):
    df = import_data
    
    # select required rows
    selected_rows = df[df['name'] == 'Rick']
    
    # Get the indices of the selected rows
    selected_indices = selected_rows.index
    selected_indices = selected_indices[selected_indices != 0]
    previous_indices = selected_indices - 1

    # Input Rows
    dfInp = df.loc[previous_indices]
    # Output Rows
    dfOp = df.loc[selected_indices]

    # Filter Input
    dfInp.columns = ['Name', 'Input']
    dfInp = dfInp.drop(['Name'], axis=1)
    dfInp = dfInp.reset_index(drop=True)

    # Filter Output
    dfOp.columns = ['Name', 'Output']
    dfOp = dfOp.drop(['Name'], axis=1)
    dfOp = dfOp.reset_index(drop=True)

    # Create Final Dataframe
    dfInp = dfInp.join(dfOp['Output'])
    return dfInp

def remove_punctuation(text):
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Return preprocessed text
    return text

@asset
def preprocess_text(filter_data):
    dfInp = filter_data

    dfInp['Input'].to_csv(os.getenv('INPUT_DATA'), index=False)

    dfInp['Input'] = dfInp['Input'].apply(remove_punctuation)
    dfInp['Output'] = dfInp['Output'].apply(remove_punctuation)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(dfInp['Input'])
    y = dfInp['Output']
    
    return X,y

@asset
def fit_model(preprocess_text):
    X,y = preprocess_text
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    svm = SVC()
    svm.fit(X_train, y_train)

    return svm

@asset
def export_model(fit_model):
    now = datetime.now()
    name = "model_" + now.strftime("%m_%d_%Y_%H_%M_%S") + ".pkl"
    filename = os.getenv('MODEL_PATH') + name
    pickle.dump(fit_model, open(filename, 'wb'))
    filename = os.getenv('MODEL_LATEST')
    pickle.dump(fit_model, open(filename, 'wb'))

