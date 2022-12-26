import re
import pickle
import pandas as pd
import os
from unidecode import unidecode
import nltk

nltk.download('punkt')

class Preprocessing():
    def __init__(self) -> None:
        with open(os.path.join("models", "vect.pkl"), 'rb') as f:
            self.vect = pickle.load(f)
        
        with open(os.path.join("models", "count_vect.pkl"), 'rb') as f:
            self.count_vect = pickle.load(f)
            
        with open(os.path.join("models", "transformer.pkl"), 'rb') as f:
            self.transformer = pickle.load(f)

    def cleaningText(self, text) -> str:
        text = re.sub(r"[^\w\d\s]", "", text)
        text = unidecode(text)
        text = re.sub(r"\\x[A-Za-z0-9./]", "", unidecode(text))
        text = re.sub('\n', '', text)
        return text
    
    def tokenize(self, text) -> str:
        tokenisasi = nltk.word_tokenize(text)
        return tokenisasi

    def slangWord(self,text) -> str:
        content = []
        kamus_slangword = eval(open("prepro/slangword.txt").read())  # Membuka dictionary slangword
        pattern = re.compile(r'\b( ' + '|'.join(kamus_slangword.keys()) + r')\b')  # Search pola kata (contoh kpn -> kapan)
        for kata in text:
            filteredSlang = pattern.sub(lambda x: kamus_slangword[x.group()],kata)  # Replace slangword berdasarkan pola review yg telah ditentukan
            content.append(filteredSlang.lower())
        text = ' '.join(content)
        return text
    
    def getVect(self, text):
        text = text.lower()
        text = self.cleaningText(text)
        text = self.tokenize(text)
        text = self.slangWord(text)
        clean_text = text
        new_df = pd.DataFrame([text],columns=['text'])
        target_predict = self.count_vect.transform(new_df['text'])
        target_predict = self.transformer.transform(target_predict)
        return clean_text,target_predict