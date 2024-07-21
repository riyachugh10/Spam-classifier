from fastapi import FastAPI
import streamlit as st
import requests
import pickle
import string
import sklearn
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()


def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

app=FastAPI()

@app.get("/")
async def root():
    return "THIS IS THE API FOR SPAM DETECTION"

@app.get("/sms_spam_Detection")
async def ma():
    return "THIS IS THE API FOR SPAM DETECTION"

@app.get("/sms_spam_Detection/{sms}")
async def get_random(sms):
        # 1. preprocess
    print(sms)
    transformed_sms = transform_text(sms)
    # 2. vectorize
    vector_input = tfidf.transform([transformed_sms])
    # 3. predict
    result = model.predict(vector_input)
    # 4. Display
    if result == 1:
       return "The Message you entered is most probably a Spam"
    else:
        return "The Message you entered is Not a Spam"

@app.get("/sms_spam_Detection/post")
async def mj():
    print()

