import os
from openai import OpenAI
import json
import gensim
from gensim.models import Word2Vec
import re


#TRAINING THE MACHINE:
import nltk

import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download()

nltk.download('punkt')  # Download the Punkt tokenizer models if not already downloaded
from nltk.tokenize import sent_tokenize


with open("/Users/sadhvinarayanan/Downloads/5C_Events/p-5cevents/services/nlp/chirp_output2.txt", "rb") as f:
        text = f.read().decode("utf-8")
paragraph = text

sentences = sent_tokenize(paragraph)

clean_txt = []

# Print the sentences
for sentence in sentences:

    desc = sentence.lower()

#remove punctuation
    desc = re.sub('[^a-zA-Z]', ' ', desc)

#remove tags
    desc=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",desc)

#remove digits and special chars
    desc=re.sub("(\\d|\\W)+"," ",desc)

    clean_txt.append(desc)
    
corpus = []
for col in clean_txt:
    word_list = col.split(" ")
    corpus.append(word_list)

word2vec_model = Word2Vec(corpus, min_count=1, vector_size = 70)
# Load pre-trained Word2Vec model
    #word2vec_model = Word2Vec.load('/Users/sadhvinarayanan/Downloads/5C_Events/p-5cevents/services/nlp/word2vec_model.bin')

word2vec_model.save("/Users/sadhvinarayanan/Downloads/5C_Events/p-5cevents/services/nlp/word2vec_model.bin")