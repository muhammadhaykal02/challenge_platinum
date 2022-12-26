import streamlit as st
import requests
import pandas as pd
from streamlit_option_menu import option_menu


def call_api_text(text, path):
    url = f"http://127.0.0.1:1010/{path}/v1"

    data_payload = {
        "text":text
    }

    response = requests.post(url,json=data_payload)
    result = response.json()
    return result

def call_api_file(uploaded_file, path):
    url = f"http://127.0.0.1:1010/{path}/v1"

    df = pd.read_csv(uploaded_file, encoding="ISO-8859-1", sep=",")
    uploaded_file = {'file': df.to_csv(index=False)}
    response = requests.post(url, files=uploaded_file)
    result = response.json()
    return result


st.title('Sentiment Analysis')

selected = option_menu(
    menu_title='Select Input', 
    options=['Text', 'File'], 
    orientation="horizontal"
    )

if selected == 'Text':
    text = st.text_input('Masukkan kalimat dalam Bahasa Indonesia')
    if text:
        path = 'ann_predict/text'
        result = call_api_text(text,path)
        st.write("Result: ", result)
else:
    uploaded_file = st.file_uploader("Masukkan file CSV yang akan diprediksi",type=['csv'])
    if uploaded_file:
        path = 'ann_predict/file'
        result = call_api_file(uploaded_file,path)
        st.write("Result: ", result)
