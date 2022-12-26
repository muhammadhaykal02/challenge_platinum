from flask import Flask, request, jsonify
from prepro.preprocessing import Preprocessing
from predict.predict import predictSentiment
import pandas as pd
import sqlite3

app = Flask(__name__)

cleanText = Preprocessing()
predictModel = predictSentiment() 

conn = sqlite3.connect("db_predict_ann.db", check_same_thread=False)


@app.route("/ann_predict/text/v1", methods=['POST'])
def predict_text():
    text = request.get_json()
    clean_text,vect = cleanText.getVect(text["text"])
    result = predictModel.predict(vect)
    return jsonify({"Sentiment":result, "Text": clean_text})

@app.route("/ann_predict/file/v1", methods=['POST'])
def predict_text_file():
    file_input = request.files['file']
    df = pd.read_csv(file_input, encoding="ISO-8859-1", sep=",")
    mycur = conn.cursor()    
    mycur.execute("DROP TABLE IF EXISTS predictSentiment")
    mycur.execute("CREATE TABLE IF NOT EXISTS predictSentiment(cleanText varchar(100), sentiment varchar(10))")
    data = []
    for index, row in df.iterrows():
        text = row['Tweet']
        clean_text,vect = cleanText.getVect(text)
        result = predictModel.predict(vect)
        
        mycur.execute("INSERT INTO predictSentiment(cleanText,sentiment) VALUES(?,?)", [clean_text,result])
        conn.commit()
    resp = jsonify({'message' : 'File successfully uploaded'})
    resp.status_code = 201
    return resp

if __name__ == "__main__":
    app.run(port=1010, debug=True)