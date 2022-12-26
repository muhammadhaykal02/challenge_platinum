import re
import pandas as pd
from unidecode import unidecode

kamus_normalisasi = pd.read_csv('Data/new_kamusalay.csv', names = ['sebelum', 'sesudah'], encoding='ISO-8859-1')

def lowerCase(i):
    return i.lower()

def remove_url(i):
    i = re.sub(r"http\S+", "", i)
    i = re.sub(r"www.\S+", "", i)
    return i

def remove_punct(i):
    i = re.sub(r"[^\w\d\s]+", "", i) 
    return i

def remove_other_body(i):
    i = re.sub(r"rt", "", i) 
    i = re.sub(r"user", "", i) 
    i = re.sub(r"[^\x00-\x7f]", r"", i) 
    return i

def remove_other_file(i): 
    i = re.sub(r"rt", "", i)
    i = re.sub(r"user", "", i)
    return re.sub(r"\\x[A-Za-z0-9./]+", "", unidecode(i))

def remove_hashtag(i):
    # i = re.sub("@[A-Za-z0-9_]+","", i)
    # i = re.sub("#[A-Za-z0-9_]+","", i)
    i = re.sub(r'#([^\s]+)',' ',i)
    i = re.sub(r'@([^\s]+)',' ',i)
    return i

def remove_multipleSpace(i):
    i = re.sub(' +', ' ', i)
    # i = re.sub("\s\s+", " ", i)
    return i

def _normalization(i):
    words = i.split()
    clear_words = ""
    for val in words:
        x = 0
        for idx, data in enumerate(kamus_normalisasi['sebelum']):
            if(val == data):
                clear_words += kamus_normalisasi['sesudah'][idx] + ' '
                print("Transform :",data,"-",kamus_normalisasi['sesudah'][idx])
                x = 1
                break
        if(x == 0):
            clear_words += val + ' '
    return clear_words