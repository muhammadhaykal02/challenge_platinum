import gradio as gr
import pandas as pd
from predict_LSTM import predictText_LSTM

def predict(text):
    result_LSTM = predictText_LSTM(text)
    d = {'text': [text], 'result_LSTM': [result_LSTM]}
    df = pd.DataFrame(data=d)
    return df

text_input = gr.Textbox(label="text")

gradio_ui = gr.Interface(
    fn=predict,
    title="Predict Text Sentiment",
    inputs=[text_input],
    outputs=[gr.components.Dataframe(label="Result")]
)

gradio_ui.launch() 