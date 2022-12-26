from flask import Flask, request, jsonify
from flasgger import Swagger, LazyString, LazyJSONEncoder, swag_from
import pandas as pd
import time
from cleansing_LSTM import lowerCase, remove_url, remove_punct, remove_other_body, remove_other_file, remove_multipleSpace, remove_hashtag, _normalization
from predict_LSTM import predictText_LSTM, predictFile_LSTM
from databaseLSTM import Input_DB_text_LSTM, Input_DB_file_LSTM

app = Flask(__name__)
app.json_encoder = LazyJSONEncoder

swagger_template = dict(
    info = {
        'title': LazyString(lambda: 'API TESTER'),
        'version': LazyString(lambda: '1'),
        'description': LazyString(lambda: 'API Tester for challenge')
    },
    host = LazyString(lambda: request.host)
)

swagger_config = {
    "headers":[],
    "specs": [
        {
            "endpoint":"docs",
            "route":"/docs.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True
        }
    ],
    "static_url_path":"/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger = Swagger(app, template=swagger_template,config=swagger_config)

def text_processing(s):
    text = s
    s = lowerCase(s)
    s = remove_url(s)
    s = remove_other_body(s)
    s = remove_hashtag(s)
    s = remove_punct(s)
    s = _normalization(s)
    s = remove_multipleSpace(s)
    # _insertText(text, s)
    return s

def file_processing(df):
    df['lower'] = df['Tweet'].apply(lowerCase)
    df['link'] = df['lower'].apply(remove_url)
    df['binary'] = df['link'].apply(remove_other_file)
    df['hastag'] = df['binary'].apply(remove_hashtag)
    df['punct'] = df['hastag'].apply(remove_punct)
    df['normalization'] = df['punct'].apply(_normalization)
    df['space'] = df['normalization'].apply(remove_multipleSpace)
    df_clean = pd.DataFrame(df[['Tweet','space']])
    # _insertFile(df_clean)
    return df

@swag_from("challenge_swagger_text.yml", methods=['POST'])
@app.route("/api/lstm/text/v1", methods=['POST'])
def predict_text_LSTM():
    text = request.get_json()
    clean_text = text_processing(text['text'])
    result = predictText_LSTM(clean_text)
    Input_DB_text_LSTM(clean_text, result)
    return jsonify({"text" : clean_text, "result":result})

@swag_from("challenge_swagger_file.yml", methods=['POST'])
@app.route("/api/lstm/file/v1", methods=['POST'])
def file_clean():
    count_time = time.time()
    file = request.files['file']
    df = pd.read_csv(file, names=['text'], encoding='ISO-8859-1')
    df['label'] = predictFile_LSTM(df)
    Input_DB_file_LSTM(df)
    return jsonify({"result":"file telah berhasil terupload", "time_exc":"%s second" % (time.time() - count_time)})

if __name__ == '__main__':
    app.run(port=1234, debug=True)

