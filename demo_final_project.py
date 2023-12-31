# -*- coding: utf-8 -*-
"""DEMO Final Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13RDErsm3vF-YErMcUDoXDAngj7ls5-wh

# Import Library & Function
"""

# Commented out IPython magic to ensure Python compatibility.
from google.colab import drive
drive.mount('/content/drive')
# %cd /content/drive/My Drive/TUGAS AKHIR/Labeled

# Commented out IPython magic to ensure Python compatibility.
# DataFrame
import pandas as pd

# Matplot
import matplotlib.pyplot as plt
# %matplotlib inline

# Scikit-learn
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split

#Evaluation Metric
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import accuracy_score, f1_score
from sklearn.metrics import recall_score, precision_score

#Model
from sklearn.pipeline import make_pipeline, Pipeline

# Keras
from keras.models import Sequential
from keras.layers import Activation, Dense, Dropout, Embedding, Flatten, Conv1D, MaxPooling1D, LSTM, SpatialDropout1D
from keras import utils
from sklearn.preprocessing import LabelEncoder
from keras.callbacks import ReduceLROnPlateau, EarlyStopping

# Feature Extraction
import gensim #Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer #TF-IDF

# nltk
import nltk
from nltk.corpus import stopwords

#Tokenizer
from keras.preprocessing.text import Tokenizer

# Utility
import numpy as np
import os
from collections import Counter
import logging
import time
import pickle
import itertools
import requests

"""## Stemming function"""

!pip install Sastrawi #Indonesian word stemmer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
# create stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

"""## Remove Punctuation Function"""

import string
string.punctuation
def remove_punctuation(text):
    punctuationfree="".join([i for i in text if i not in string.punctuation])
    return punctuationfree

"""## Tokenization function"""

import re
def tokenization(text):
    return nltk.word_tokenize(text)

"""## Stopword & NLP library"""

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')

# CONSTRUCT STOPWORDS
rama_stopword = "https://raw.githubusercontent.com/ramaprakoso/analisis-sentimen/master/kamus/stopword.txt"
yutomo_stopword = "https://raw.githubusercontent.com/yasirutomo/python-sentianalysis-id/master/data/feature_list/stopwordsID.txt"
fpmipa_stopword = "https://raw.githubusercontent.com/onlyphantom/elangdev/master/elang/word2vec/utils/stopwords-list/fpmipa-stopwords.txt"
sastrawi_stopword = "https://raw.githubusercontent.com/onlyphantom/elangdev/master/elang/word2vec/utils/stopwords-list/sastrawi-stopwords.txt"
aliakbar_stopword = "https://raw.githubusercontent.com/onlyphantom/elangdev/master/elang/word2vec/utils/stopwords-list/aliakbars-bilp.txt"
pebahasa_stopword = "https://raw.githubusercontent.com/onlyphantom/elangdev/master/elang/word2vec/utils/stopwords-list/pebbie-pebahasa.txt"
elang_stopword = "https://raw.githubusercontent.com/onlyphantom/elangdev/master/elang/word2vec/utils/stopwords-id.txt"
nltk_stopword = stopwords.words('indonesian')

# create path url for each stopword
path_stopwords = [rama_stopword, yutomo_stopword, fpmipa_stopword, sastrawi_stopword,
                  aliakbar_stopword, pebahasa_stopword, elang_stopword]

# combine stopwords
stopwords_l = nltk_stopword
for path in path_stopwords:
    response = requests.get(path)
    stopwords_l += response.text.split('\n')

#Slang word
slang = '''
yg yang dgn ane smpai bgt gua gwa si tu ama utk udh btw
ntar lol ttg emg aj aja tll sy sih kalo nya trsa mnrt nih
ma dr ajaa tp akan bs bikin kta pas pdahl bnyak guys abis tnx
bang banget nang mas amat bangettt tjoy hemm haha sllu hrs lanjut
bgtu sbnrnya trjadi bgtu pdhl sm plg skrg
'''

# create dictionary with unique stopword
st_words = set(stopwords_l)
slang_word = set(slang.split())

# result stopwords
stop_words = st_words | slang_word
print(f'Stopwords: {list(stop_words)[:5]}')
print(len(stop_words))

def remove_stopwords(text):
    output= [i for i in text if i not in stop_words]
    return output

def preprocess_text(text, lst_stopwords=None):
    ## clean (convert to lowercase and remove punctuations and characters and then strip)
    text = re.sub(r'[^\w\s]', '', str(text).lower().strip())

    ## Tokenize (convert from string to list)
    lst_text = text.split()
    ## remove Stopwords
    if lst_stopwords is not None:
        lst_text = remove_stopwords(lst_text)

    ## Stemming (remove -ing, -ly, ...)
    lst_text = [stemmer.stem(word) for word in lst_text]

    ## back to string from list
    text = " ".join(lst_text)
    return text

"""# Preprocess Function Breakdown"""

data2 = pd.read_csv('Dataset Labeled.csv')
data2['clean_msg'] = data2['text'].apply(lambda x:remove_punctuation(x))
data2['msg_lower']= data2['clean_msg'].apply(lambda x: x.lower())
data2['stemmed']= data2['msg_lower'].apply(lambda x:stemmer.stem(x))
data2['tokenized']= data2.apply(lambda row: nltk.word_tokenize(row['stemmed']), axis=1)
data2['no_stopwords']= data2['tokenized'].apply(lambda x:remove_stopwords(x))

from random import randrange
idx = randrange(len(data2))

pd.set_option('max_colwidth', 500)
print(data2.loc[idx])

"""#Read Data

## Data Balance Check
"""

data = pd.read_csv('Dataset Labeled.csv')
data.head()

label = Counter(data.label)
print(label.keys(),label.values())

plt.figure(figsize=(16,8))
plt.bar(label.keys(), label.values())
plt.title("Dataset labels distribuition")

"""## Preprocessing"""

data["text_clean"] = data["text"].apply(lambda x: preprocess_text(x, lst_stopwords=stop_words))

data.head()

data.to_csv('dataset_processed.csv')

"""# 70:30 Ratio

## Split Data
"""

train_data, test_data = train_test_split(data, test_size=0.3, random_state=42)

"""## SVM"""

vectorizer = TfidfVectorizer(
    min_df = 5,
    max_df = 0.8,
    sublinear_tf = True,
    use_idf = True)

corpus = train_data['text_clean']

vectorizer.fit(corpus)
X_train = vectorizer.transform(corpus)
dic_vocabulary = vectorizer.vocabulary_

X_test = vectorizer.transform(test_data['text_clean'].values)

y_train = train_data["label"].values
y_test = test_data["label"].values

print("TRAIN size:", len(train_data))
print("TEST size:", len(test_data))

classifier = SVC(kernel='linear', probability=True)
# pipeline
model = Pipeline([("vectorizer", vectorizer),  ("classifier", classifier)])

#Train & Test
t0 = time.time()
model["classifier"].fit(X_train, y_train)
t1 = time.time()
y_predict = classifier.predict(X_test)
t2 = time.time()

prediction_prob = model.predict_proba(list(test_data['text_clean']))

"""### Evaluate"""

# Commented out IPython magic to ensure Python compatibility.
accuracy = accuracy_score(y_test, y_predict)
recall = recall_score(y_test, y_predict)
precision = precision_score(y_test, y_predict)
f1 = f1_score(y_test, y_predict)
print("Accuracy:",  accuracy)
print("Recall:",  recall)
print("Precision:",  precision)
print("F1-Score:",  f1)
print("Detail:")
print(classification_report(y_test, y_predict))

import seaborn as sns
#mengimplementasikan testing data dan hasil prediksi ke dalam confusion matrix
cm = confusion_matrix(y_test, y_predict)

#membuat plotting confusion matrix
# %matplotlib inline
plt.figure (figsize=(10,7))
sns.heatmap(cm, annot=True, fmt='d')
plt.xlabel('Predicted')
plt.ylabel('Truth')

"""## LSTM"""

#Parameters

# WORD2VEC
W2V_SIZE = 300
W2V_WINDOW = 7
W2V_EPOCH = 32
W2V_MIN_COUNT = 10

# KERAS / Model
SEQUENCE_LENGTH = 300
EPOCHS = 16
BATCH_SIZE = 32

"""### Building Vocabulary"""

w2v_model = gensim.models.word2vec.Word2Vec(size=W2V_SIZE,
                                            window=W2V_WINDOW,
                                            min_count=W2V_MIN_COUNT,
                                            workers=8)


documents = [_text.split() for _text in train_data.text]
w2v_model.build_vocab(documents)

words = w2v_model.wv.vocab.keys()
vocab_size = len(words)
print("Vocab size", vocab_size)

w2v_model.train(documents, total_examples=len(documents), epochs=W2V_EPOCH)

w2v_model.most_similar("suka")

tokenizer = Tokenizer()
tokenizer.fit_on_texts(train_data.text)

vocab_size = len(tokenizer.word_index) + 1
print("Total words", vocab_size)

from keras_preprocessing.sequence import pad_sequences

x_train = pad_sequences(tokenizer.texts_to_sequences(train_data.text_clean), maxlen=SEQUENCE_LENGTH)
x_test = pad_sequences(tokenizer.texts_to_sequences(test_data.text_clean), maxlen=SEQUENCE_LENGTH)

labels = train_data.label.unique().tolist()
labels

encoder = LabelEncoder()
encoder.fit(train_data.label.tolist())

y_train = encoder.transform(train_data.label.tolist())
y_test = encoder.transform(test_data.label.tolist())

y_train = y_train.reshape(-1,1)
y_test = y_test.reshape(-1,1)

print("y_train",y_train.shape)
print("y_test",y_test.shape)

"""### Word Embedding Matrix"""

embedding_matrix = np.zeros((vocab_size, W2V_SIZE))
for word, i in tokenizer.word_index.items():
  if word in w2v_model.wv:
    embedding_matrix[i] = w2v_model.wv[word]
print(embedding_matrix.shape)

embedding_layer = Embedding(vocab_size, W2V_SIZE, weights=[embedding_matrix], input_length=SEQUENCE_LENGTH, trainable=False)

model2 = Sequential()
model2.add(embedding_layer)
model2.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
model2.add(Dropout(0.5))
model2.add(Dense(1, activation='relu'))
model2.add(Dropout(0.2))
model2.add(Dense(4,activation='softmax'))

model2.compile(loss='sparse_categorical_crossentropy',
               optimizer='adam',
               metrics=['accuracy'])


print(model2.summary())

callbacks = [ ReduceLROnPlateau(monitor='val_loss', patience=5, cooldown=0),
              EarlyStopping(monitor='val_accuracy', min_delta=1e-4, patience=5)]

history = model2.fit(x_train, y_train,
                    batch_size=BATCH_SIZE,
                    epochs=16,
                    validation_split=0.1,
                    verbose=1,
                    callbacks=callbacks)

"""### Evaluate"""

## encode y
dic_y_mapping = {n:label for n,label in
                 enumerate(np.unique(y_train))}
## test
predicted_prob = model2.predict(x_test)
predicted = [dic_y_mapping[np.argmax(pred)] for pred in
             predicted_prob]

classes = np.unique(y_test)

## Accuracy, Precision, Recall
accuracy = accuracy_score(y_test, predicted)
recall = recall_score(y_test, predicted)
precision = precision_score(y_test, predicted)
f1 = f1_score(y_test, predicted)
print("Accuracy:",  accuracy)
print("Recall:",  recall)
print("Precision:",  precision)
print("F1-Score:",  f1)
print("Detail:")
print(classification_report(y_test, predicted))

## Plot confusion matrix
cm = confusion_matrix(y_test, predicted)
fig, ax = plt.subplots()
sns.heatmap(cm, annot=True, fmt='d', ax=ax, cmap=plt.cm.Blues,
            cbar=False)
ax.set(xlabel="Pred", ylabel="True", xticklabels=classes,
       yticklabels=classes, title="Confusion matrix")
plt.yticks(rotation=0)

"""# 80:20

## Split Data
"""

train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

"""## SVM"""

vectorizer = TfidfVectorizer(
    min_df = 5,
    max_df = 0.8,
    sublinear_tf = True,
    use_idf = True)

corpus = train_data['text_clean']

vectorizer.fit(corpus)
X_train = vectorizer.transform(corpus)
dic_vocabulary = vectorizer.vocabulary_

X_test = vectorizer.transform(test_data['text_clean'].values)

y_train = train_data["label"].values
y_test = test_data["label"].values

print("TRAIN size:", len(train_data))
print("TEST size:", len(test_data))

word = "suka"
dic_vocabulary[word]

classifier = SVC(kernel='linear', probability=True)
# pipeline
model2 = Pipeline([("vectorizer", vectorizer),  ("classifier", classifier)])

#Train & Test
t0 = time.time()
model2["classifier"].fit(X_train, y_train)
t1 = time.time()
y_predict = classifier.predict(X_test)
t2 = time.time()

prediction_prob = model2.predict_proba(list(test_data['text_clean']))

"""### Evaluate"""

# Commented out IPython magic to ensure Python compatibility.
accuracy = accuracy_score(y_test, y_predict)
recall = recall_score(y_test, y_predict)
precision = precision_score(y_test, y_predict)
f1 = f1_score(y_test, y_predict)
print("Accuracy:",  accuracy)
print("Recall:",  recall)
print("Precision:",  precision)
print("F1-Score:",  f1)
print("Detail:")
print(classification_report(y_test, y_predict))

import seaborn as sns
#mengimplementasikan testing data dan hasil prediksi ke dalam confusion matrix
cm = confusion_matrix(y_test, y_predict)

#membuat plotting confusion matrix
# %matplotlib inline
plt.figure (figsize=(10,7))
sns.heatmap(cm, annot=True, fmt='d')
plt.xlabel('Predicted')
plt.ylabel('Truth')

"""## LSTM"""

#Parameters

# WORD2VEC
W2V_SIZE = 300
W2V_WINDOW = 7
W2V_EPOCH = 32
W2V_MIN_COUNT = 10

# KERAS
SEQUENCE_LENGTH = 300
EPOCHS = 32
BATCH_SIZE = 32

# SENTIMENT
POSITIVE = "POSITIVE"
NEGATIVE = "NEGATIVE"
NEUTRAL = "NEUTRAL"
SENTIMENT_THRESHOLDS = (0.4, 0.7)

# EXPORT
KERAS_MODEL = "model.h5"
WORD2VEC_MODEL = "model.w2v"
TOKENIZER_MODEL = "tokenizer.pkl"
ENCODER_MODEL = "encoder.pkl"

"""### Building Vocabulary"""

w2v_model = gensim.models.word2vec.Word2Vec(size=W2V_SIZE,
                                            window=W2V_WINDOW,
                                            min_count=W2V_MIN_COUNT,
                                            workers=8)


documents = [_text.split() for _text in train_data.text]
w2v_model.build_vocab(documents)

words = w2v_model.wv.vocab.keys()
vocab_size = len(words)
print("Vocab size", vocab_size)

w2v_model.train(documents, total_examples=len(documents), epochs=W2V_EPOCH)

w2v_model.most_similar("suka")

tokenizer = Tokenizer()
tokenizer.fit_on_texts(train_data.text)

vocab_size = len(tokenizer.word_index) + 1
print("Total words", vocab_size)

from keras_preprocessing.sequence import pad_sequences

x_train = pad_sequences(tokenizer.texts_to_sequences(train_data.text_clean), maxlen=SEQUENCE_LENGTH)
x_test = pad_sequences(tokenizer.texts_to_sequences(test_data.text_clean), maxlen=SEQUENCE_LENGTH)

labels = train_data.label.unique().tolist()
labels

encoder = LabelEncoder()
encoder.fit(train_data.label.tolist())

y_train = encoder.transform(train_data.label.tolist())
y_test = encoder.transform(test_data.label.tolist())

y_train = y_train.reshape(-1,1)
y_test = y_test.reshape(-1,1)

print("y_train",y_train.shape)
print("y_test",y_test.shape)

"""### Word Embedding Matrix"""

embedding_matrix = np.zeros((vocab_size, W2V_SIZE))
for word, i in tokenizer.word_index.items():
  if word in w2v_model.wv:
    embedding_matrix[i] = w2v_model.wv[word]
print(embedding_matrix.shape)

embedding_layer = Embedding(vocab_size, W2V_SIZE, weights=[embedding_matrix], input_length=SEQUENCE_LENGTH, trainable=False)

model3 = Sequential()
model3.add(embedding_layer)
model3.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
model3.add(Dropout(0.5))
model3.add(Dense(1, activation='relu'))
model3.add(Dropout(0.2))
model3.add(Dense(4,activation='softmax'))

model3.compile(loss='sparse_categorical_crossentropy',
               optimizer='adam',
               metrics=['accuracy'])


print(model3.summary())

callbacks = [ ReduceLROnPlateau(monitor='val_loss', patience=5, cooldown=0),
              EarlyStopping(monitor='val_accuracy', min_delta=1e-4, patience=5)]

history = model3.fit(x_train, y_train,
                    batch_size=BATCH_SIZE,
                    epochs=16,
                    validation_split=0.1,
                    verbose=1,
                    callbacks=callbacks)

"""### Evaluate"""

## encode y
dic_y_mapping = {n:label for n,label in
                 enumerate(np.unique(y_train))}
## test
predicted_prob = model3.predict(x_test)
predicted = [dic_y_mapping[np.argmax(pred)] for pred in
             predicted_prob]

classes = np.unique(y_test)

## Accuracy, Precision, Recall
accuracy = accuracy_score(y_test, predicted)
recall = recall_score(y_test, predicted)
precision = precision_score(y_test, predicted)
f1 = f1_score(y_test, predicted)
print("Accuracy:",  accuracy)
print("Recall:",  recall)
print("Precision:",  precision)
print("F1-Score:",  f1)
print("Detail:")
print(classification_report(y_test, predicted))

## Plot confusion matrix
cm = confusion_matrix(y_test, predicted)
fig, ax = plt.subplots()
sns.heatmap(cm, annot=True, fmt='d', ax=ax, cmap=plt.cm.Blues,
            cbar=False)
ax.set(xlabel="Pred", ylabel="True", xticklabels=classes,
       yticklabels=classes, title="Confusion matrix")
plt.yticks(rotation=0)

"""# 90:10 Ratio

## Split Data
"""

train_data, test_data = train_test_split(data, test_size=0.1, random_state=42)

"""## SVM"""

vectorizer = TfidfVectorizer(
    min_df = 5,
    max_df = 0.8,
    sublinear_tf = True,
    use_idf = True)

corpus = train_data['text_clean']

vectorizer.fit(corpus)
X_train = vectorizer.transform(corpus)
dic_vocabulary = vectorizer.vocabulary_

X_test = vectorizer.transform(test_data['text_clean'].values)

y_train = train_data["label"].values
y_test = test_data["label"].values

print("TRAIN size:", len(train_data))
print("TEST size:", len(test_data))

word = "suka"
dic_vocabulary[word]

classifier = SVC(kernel='linear', probability=True)
# pipeline
model = Pipeline([("vectorizer", vectorizer),  ("classifier", classifier)])

#Train & Test
t0 = time.time()
model["classifier"].fit(X_train, y_train)
t1 = time.time()
y_predict = classifier.predict(X_test)
t2 = time.time()

prediction_prob = model.predict_proba(list(test_data['text_clean']))

"""### Evaluate"""

# Commented out IPython magic to ensure Python compatibility.
accuracy = accuracy_score(y_test, y_predict)
recall = recall_score(y_test, y_predict)
precision = precision_score(y_test, y_predict)
f1 = f1_score(y_test, y_predict)
print("Accuracy:",  accuracy)
print("Recall:",  recall)
print("Precision:",  precision)
print("F1-Score:",  f1)
print("Detail:")
print(classification_report(y_test, y_predict))

import seaborn as sns
#mengimplementasikan testing data dan hasil prediksi ke dalam confusion matrix
cm = confusion_matrix(y_test, y_predict)

#membuat plotting confusion matrix
# %matplotlib inline
plt.figure (figsize=(10,7))
sns.heatmap(cm, annot=True, fmt='d')
plt.xlabel('Predicted')
plt.ylabel('Truth')

"""## LSTM"""

#Parameters

# WORD2VEC
W2V_SIZE = 300
W2V_WINDOW = 7
W2V_EPOCH = 32
W2V_MIN_COUNT = 10

# KERAS
SEQUENCE_LENGTH = 300
EPOCHS = 32
BATCH_SIZE = 32

"""### Building Vocabulary"""

w2v_model = gensim.models.word2vec.Word2Vec(size=W2V_SIZE,
                                            window=W2V_WINDOW,
                                            min_count=W2V_MIN_COUNT,
                                            workers=8)


documents = [_text.split() for _text in train_data.text]
w2v_model.build_vocab(documents)

words = w2v_model.wv.vocab.keys()
vocab_size = len(words)
print("Vocab size", vocab_size)

w2v_model.train(documents, total_examples=len(documents), epochs=W2V_EPOCH)

w2v_model.most_similar("suka")

tokenizer = Tokenizer()
tokenizer.fit_on_texts(train_data.text)

vocab_size = len(tokenizer.word_index) + 1
print("Total words", vocab_size)

from keras_preprocessing.sequence import pad_sequences

x_train = pad_sequences(tokenizer.texts_to_sequences(train_data.text_clean), maxlen=SEQUENCE_LENGTH)
x_test = pad_sequences(tokenizer.texts_to_sequences(test_data.text_clean), maxlen=SEQUENCE_LENGTH)

labels = train_data.label.unique().tolist()
labels

encoder = LabelEncoder()
encoder.fit(train_data.label.tolist())

y_train = encoder.transform(train_data.label.tolist())
y_test = encoder.transform(test_data.label.tolist())

y_train = y_train.reshape(-1,1)
y_test = y_test.reshape(-1,1)

print("y_train",y_train.shape)
print("y_test",y_test.shape)

"""### Word Embedding Matrix"""

embedding_matrix = np.zeros((vocab_size, W2V_SIZE))
for word, i in tokenizer.word_index.items():
  if word in w2v_model.wv:
    embedding_matrix[i] = w2v_model.wv[word]
print(embedding_matrix.shape)

embedding_layer = Embedding(vocab_size, W2V_SIZE, weights=[embedding_matrix], input_length=SEQUENCE_LENGTH, trainable=False)

model2 = Sequential()
model2.add(embedding_layer)
model2.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
model2.add(Dropout(0.5))
model2.add(Dense(1, activation='relu'))
model2.add(Dropout(0.2))
model2.add(Dense(4,activation='softmax'))

model2.compile(loss='sparse_categorical_crossentropy',
               optimizer='adam',
               metrics=['accuracy'])


print(model2.summary())

callbacks = [ ReduceLROnPlateau(monitor='val_loss', patience=5, cooldown=0),
              EarlyStopping(monitor='val_accuracy', min_delta=1e-4, patience=5)]

history = model2.fit(x_train, y_train,
                    batch_size=BATCH_SIZE,
                    epochs=16,
                    validation_split=0.1,
                    verbose=1,
                    callbacks=callbacks)

"""### Evaluate"""

## encode y
dic_y_mapping = {n:label for n,label in
                 enumerate(np.unique(y_train))}
## test
predicted_prob = model2.predict(x_test)
predicted = [dic_y_mapping[np.argmax(pred)] for pred in
             predicted_prob]

classes = np.unique(y_test)

## Accuracy, Precision, Recall
accuracy = accuracy_score(y_test, predicted)
recall = recall_score(y_test, predicted)
precision = precision_score(y_test, predicted)
f1 = f1_score(y_test, predicted)
print("Accuracy:",  accuracy)
print("Recall:",  recall)
print("Precision:",  precision)
print("F1-Score:",  f1)
print("Detail:")
print(classification_report(y_test, predicted))

## Plot confusion matrix
cm = confusion_matrix(y_test, predicted)
fig, ax = plt.subplots()
sns.heatmap(cm, annot=True, fmt='d', ax=ax, cmap=plt.cm.Blues,
            cbar=False)
ax.set(xlabel="Pred", ylabel="True", xticklabels=classes,
       yticklabels=classes, title="Confusion matrix")
plt.yticks(rotation=0)

"""### Plot Confusion Matrix"""

y_predict2 = model2.predict(x_test).round()

print("Accuracy:",  round(accuracy,2))
print("Detail:")
print(classification_report(y_test, y_predict2))

# Commented out IPython magic to ensure Python compatibility.
import seaborn as sns
#mengimplementasikan testing data dan hasil prediksi ke dalam confusion matrix
cm = confusion_matrix(y_test, y_predict2)

#membuat plotting confusion matrix
# %matplotlib inline
plt.figure (figsize=(10,7))
sns.heatmap(cm, annot=True, fmt='d')
plt.xlabel('Predicted')
plt.ylabel('Truth')

