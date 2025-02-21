# -*- coding: utf-8 -*-
"""Fake-News-Detection

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tuwMTCWf1FRm9PAO5ciehPERgTPQH1td
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt

import os

# Set the search parameters
# Make sure to replace 'music1.xlsx' with actual name of your file in your directory
filename = 'train.xlsx'
search_path = '/content/sample_data/train.xlsx'

import pandas as pd

# Load the XLSX file into a DataFrame
df = pd.read_excel('/content/sample_data/train.xlsx')

df.shape
df.head()

#DataFlair - Get the labels
Label=df.Label
Label.head()

# Split dataset into features and labels
X = df['Statement']
y = df['Label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)

# Fit and transform training set, transform testing set
tfidf_train = tfidf_vectorizer.fit_transform(X_train)
tfidf_test = tfidf_vectorizer.transform(X_test)

#DataFlair - Initialize a PassiveAggressiveClassifier
pac=PassiveAggressiveClassifier(max_iter=50)
pac.fit(tfidf_train,y_train)

#DataFlair - Predict on the test set and calculate accuracy
y_pred=pac.predict(tfidf_test)
score=accuracy_score(y_test,y_pred)
print(f'Accuracy: {round(score*100,2)}%')

# Confusion matrix
confusion_mat = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:\n", confusion_mat)

# Visualize confusion matrix
plt.matshow(confusion_mat, cmap=plt.cm.gray)
plt.show()

# Initialize Passive Aggressive Classifier with different hyperparameters
pac = PassiveAggressiveClassifier(max_iter=100, C=0.1)
pac.fit(tfidf_train, y_train)
y_pred = pac.predict(tfidf_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Initialize TfidfVectorizer with n-grams
tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english', max_df=0.7)

# Create custom features
# For example, you can include the length of the text as a feature
X_train_len = np.array([len(text) for text in X_train]).reshape(-1, 1)
X_test_len = np.array([len(text) for text in X_test]).reshape(-1, 1)

# Combine custom features with TF-IDF features
from scipy.sparse import hstack
X_train_combined = hstack((tfidf_train, X_train_len))
X_test_combined = hstack((tfidf_test, X_test_len))

def lowercase_text(text):
    return text.lower()

# Apply lowercasing to the text data
X_train_lowercased = X_train.apply(lowercase_text)
X_test_lowercased = X_test.apply(lowercase_text)

import re
import string
from nltk.corpus import stopwords

# Define function for text preprocessing
def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()

    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Remove special characters
    text = re.sub(r'\W', ' ', text)

    # Remove digits
    text = re.sub(r'\d+', ' ', text)

    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    text = ' '.join(filtered_words)

    return text