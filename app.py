import streamlit as st
import requests
import pickle
import string
import sklearn
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer
from streamlit_lottie import st_lottie

st.set_page_config(page_title="Mayank Joshi")
def load(url):
    r=requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()

lottie_coding=load("https://assets5.lottiefiles.com/packages/lf20_kLZ5DxNiU9.json")
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

st.title("Email/SMS Spam Classifier")

st_lottie(lottie_coding,height=200,key="coding")
input_sms = st.text_area("Enter the message")

if st.button('Predict'):
    if input_sms=="":
        st.header("EMPTY ,Enter a text")
    else:
        # 1. preprocess
        transformed_sms = transform_text(input_sms)
        # 2. vectorize
        vector_input = tfidf.transform([transformed_sms])
        # 3. predict
        result = model.predict(vector_input)[0]
        # 4. Display
        if result == 1:
            st.header("The Message you entered is most probably a Spam")
        else:
            st.header("The Message you entered is Not a Spam")
