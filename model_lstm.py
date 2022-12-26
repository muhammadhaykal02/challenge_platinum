# -*- coding: utf-8 -*-
"""Copy of Model LSTM Final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yzz8yGzfzctBbnLVOjManq015nyDsEYL
"""

from google.colab import files
files.upload()

import pandas as pd

df = pd.read_csv('/content/training_fix.csv',sep=';', header=0)

df = df.drop(['Unnamed: 0'], axis=1)

df['tweet'] = df['tweet'].str.replace('[^\w\s]',' ')
df['tweet'] = df['tweet'].str.replace(r'\s+', ' ', regex=True)
df['tweet'] = df['tweet'].str.replace(r'\n', ' ', regex=True)
df.head(5)

df.drop(['Unnamed: 0'], axis=1)

from collections import Counter

results = Counter()
df['tweet'].str.lower().str.split().apply(results.update)
print(len(results))

# preprocessing
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences

max_fatures = 18533
tokenizer = Tokenizer(num_words=max_fatures, split=' ')
tokenizer.fit_on_texts(df['tweet'].values) # -> bikin menu kata menjadi integer
X = tokenizer.texts_to_sequences(df['tweet'].values) # -> merubah kata menjadi integer
X = pad_sequences(X)

X.shape

from sklearn.model_selection import train_test_split

Y = pd.get_dummies(df['label']).values
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.2, random_state = 32, stratify = Y)
print(X_train.shape,Y_train.shape)
print(X_test.shape,Y_test.shape)

from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D

embed_dim = 128
lstm_out = 196

model = Sequential()
model.add(Embedding(max_fatures, embed_dim,input_length = X.shape[1]))
model.add(SpatialDropout1D(0.5))
model.add(LSTM(lstm_out, dropout=0.5, recurrent_dropout=0.5))
model.add(Dense(3,activation='softmax'))
model.compile(loss = 'categorical_crossentropy', optimizer='adam',metrics = ['accuracy'])
print(model.summary())

print(len(X_train))
print(len(Y_train))
print(len(X_test))
print(len(Y_test))

validation_size = 600

X_validate = X_test[-validation_size:]
Y_validate = Y_test[-validation_size:]
X_test = X_test[:-validation_size]
Y_test = Y_test[:-validation_size]

from keras.callbacks import EarlyStopping

earlyStop=EarlyStopping(monitor="val_loss",verbose=2,mode='min', patience=2)
history=model.fit(X_train,Y_train,epochs = 7, batch_size=256,validation_data=(X_validate,Y_validate) ,verbose=2,callbacks=[earlyStop])

score,acc = model.evaluate(X_test, Y_test, verbose = 2, batch_size = 256)
print("score: %.2f" % (score))
print("acc: %.2f" % (acc))

import numpy as np
rounded_Y_test=np.argmax(Y_test, axis=1)
rounded_Y_test[1]

Y_predict = []
for x in X_test:
  x = np.reshape(x, (1,96))
  result = model.predict(x, batch_size=64, verbose=2)[0]
  if(np.argmax(result) == 0):
    Y_predict.append(0)
  elif (np.argmax(result) == 1):
    Y_predict.append(1)
  elif (np.argmax(result) == 2):
    Y_predict.append(2)

Y_predict

from sklearn import metrics

print(metrics.classification_report(rounded_Y_test, Y_predict))

twt = ['halo dunia, apa kabar kamu?']
#vectorizing the tweet by the pre-fitted tokenizer instance
twt = tokenizer.texts_to_sequences(twt)
#padding the tweet to have exactly the same shape as `embedding_2` input
twt = pad_sequences(twt, maxlen=96, dtype='int32', value=0)
print(twt)

sentiment = model.predict(twt,batch_size=1,verbose = 2)[0]
if(np.argmax(sentiment) == 0):
    print("negative")
elif (np.argmax(sentiment) == 1):
    print("neutral")
elif (np.argmax(sentiment) == 2):
    print("positive")

import matplotlib.pyplot as plt

plt.plot(history.history['loss'], color='b', label='training loss')
plt.plot(history.history['val_loss'], color='y', label='validation loss')
plt.title('Test Loss')
plt.xlabel('Number of Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show

import matplotlib.pyplot as plt

plt.plot(history.history['accuracy'], color='b', label='training acc')
plt.plot(history.history['val_accuracy'], color='y', label='validation acc')
plt.title('Accuracy')
plt.xlabel('Number of Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show

model.save('model_lstm.h5')

import pickle

with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)