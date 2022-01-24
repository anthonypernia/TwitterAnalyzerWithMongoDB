import re
import nltk as nltk
from nltk.corpus import stopwords
from textblob import TextBlob
import pandas as pd
import emoji
nltk.download('stopwords')
nltk.download('punkt')

def remove_links_rt_hashtags(text: str):
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'https?:\/\/\S+', ' ', text) #Remover links
    text = re.sub(r'RT', '', text)
    text = re.sub(r'RT[\s]', ' ', text) # Remover RTs
    text = re.sub(r'#', '', text)
    text = re.sub(r'@[A-Za-z0-9]+', ' ', text) # Remover menciones 
    return text

def remove_puncs(text: str):
    text = re.sub(r'[,.:;()?!]', ' ', text)
    return text


def remove_stopwords(text: str):
    stop_words_en = set(stopwords.words('english'))
    stop_words_es = set(stopwords.words('spanish'))
    word_tokens = nltk.word_tokenize(text)
    filtered_sentence = [w for w in word_tokens if not w in stop_words_en and not w in stop_words_es]
    return " ".join(filtered_sentence)

def remove_emojis(text):
    return ''.join(c for c in text if c not in emoji.UNICODE_EMOJI)

def columns_to_datetime(df: pd.DataFrame, columns: list):
    for column in columns:
        df[column] = pd.to_datetime(df[column])
    return df


def transform_text(text: str):
    text = remove_links_rt_hashtags(text)
    text = remove_puncs(text)
    text = remove_stopwords(text)
    text = remove_emojis(text)
    return text

def set_sentiment(text):
    sentiment=0
    text = str(text)
    if text != '':
        analysis = TextBlob(text)
        if len(analysis)>3:
            #if analysis.detect_language() == 'es':
            #analysis = analysis.translate(from_lang='es',to='en').sentiment
            sentiment = analysis.polarity
    return sentiment