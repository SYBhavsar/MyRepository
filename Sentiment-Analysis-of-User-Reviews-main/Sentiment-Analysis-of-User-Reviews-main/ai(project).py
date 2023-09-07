# -*- coding: utf-8 -*-
"""AI(Project)

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dfRMNja6RnrIJvv3yYQrFymPJcnrvIxp
"""

import pandas as pd
import numpy as np
import nltk
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('omw-1.4')

from google.colab import files
import io


uploaded = files.upload()

df = pd.read_csv(io.BytesIO(uploaded['fkartdata.csv']))
print(df)

df['Rate'].value_counts()

print("Number of rows in data:", df.shape[0])
print("Number of columns in data:", df.shape[1])

df.Rate.value_counts()

df.isnull().sum()

df['Rate']=df['Rate'].replace(['1,2,3'],'0')
df['Rate']=df['Rate'].replace(['4,5'],'1')

df.Rate.value_counts()

X = df["Review"]
y = df["Rate"]
X.head()

"""TEXT PRE_PROCESSING"""

def stringprocess(text):
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " is", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "cannot ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r"\'scuse", " excuse ", text)
    text = re.sub('\W', ' ', text)
    text = re.sub('\s+', ' ', text)
    text = text.strip(' ')

    return text

from string import digits
import string
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

def  textpreprocess(text):

    text = map(lambda x: x.lower(), text) # Lower case
    text = map(lambda x: re.sub(r"https?://\S+|www\.\S+", "", x), text) # Remove Links
    text = map(lambda x: re.sub(re.compile(r"<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});"),"", x), text) # Remove html tags
    text = map(lambda x: re.sub(r'[^\x00-\x7f]',r' ', x), text) # Remove non-ASCII characters
    # Remove special special characters, including symbols, emojis, and other graphic characters

    emoji_pattern = re.compile(
             '['
            u'\U0001F600-\U0001F64F'  # emoticons
            u'\U0001F300-\U0001F5FF'  # symbols & pictographs
            u'\U0001F680-\U0001F6FF'  # transport & map symbols
            u'\U0001F1E0-\U0001F1FF'  # flags (iOS)
            u'\U00002702-\U000027B0'
            u'\U000024C2-\U0001F251'
            ']+',
            flags=re.UNICODE)
    text = map(lambda x: emoji_pattern.sub(r'', x), text)
    text = map(lambda x: x.translate(str.maketrans('', '', string.punctuation)), text) # Remove punctuations
    remove_digits = str.maketrans('', '', digits)
    text = [i.translate(remove_digits) for i in text]
    text = [w for w in text if not w in stop_words]
    text = ' '.join([lemmatizer.lemmatize(w) for w in text])
    text = text.strip()
    return text

X = X.apply(lambda x: stringprocess(x))
word_tokens = X.apply(lambda x: word_tokenize(x))

preprocess_text = word_tokens.apply(lambda x: textpreprocess(x))