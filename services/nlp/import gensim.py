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

with open("/Users/sadhvinarayanan/Downloads/hivDist/openai-env/chirp_output2.txt", "rb") as f:
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
#word2vec_model = Word2Vec.load('path/to/pretrained/model')


# Keywords for event tagging
keywords = ['academic', 'computer science', 'humanities', 'fellowship', 'protest', 'social justice', 'workshop', 'seminar', 'conference', 'symposium', 'panel', 'lecture', 'workshop series', 'career fair', 'networking', 'cultural', 'social', 'club', 'volunteer', 'orientation', 'recruitment', 'sports', 'party', 'wellness']

# Create vector embeddings for keywords
keyword_embeddings = {}
for keyword in keywords:
    keyword_tokens = keyword.split()  # Tokenize the keyword if it contains multiple words
    keyword_embedding = []
    for token in keyword_tokens:
        if token in word2vec_model.wv.key_to_index:
            keyword_embedding.append(word2vec_model.wv.get_vector(token))
    if keyword_embedding:
        keyword_embeddings[keyword] = sum(keyword_embedding) / len(keyword_embedding)

# Event description
#event_description = "Fellowship Information Dinner @ Frank Blue Room, Wed, 3/20 from 5:15 - 6:15 PM What exactly is a fellowship? How do you apply for one? When can you apply for one? Get your answers to these questions from the CDO Fellowship Advisor Jason Jeffrey"
#event_description = "Last Friday Claremont Police arrested 20 students at Pomona College who were conducting a sit-in, charging them with trespassing and obstruction of justice. Join Professors Shields and Kim for a discussion over this event's implications for student activism and institutional responses during Ath Tea at Adams Courtyard at the Athenaeum from 3 - 4:30 PM this Friday, April 12."
event_description = "Come talk to the Computer Science professors in the pannel for understanding computer science course registration"
# Preprocess the event description
event_description = event_description.lower().split()

# Calculate similarity between event description and each keyword
similarity_scores = {}
for keyword, embedding in keyword_embeddings.items():
    keyword_similarity = []
    for word in event_description:
        if word in word2vec_model.wv.key_to_index:
            word_embedding = word2vec_model.wv.get_vector(word)
            similarity = word2vec_model.wv.cosine_similarities(embedding, [word_embedding])
            keyword_similarity.append(max(similarity))
    if keyword_similarity:
        similarity_scores[keyword] = sum(keyword_similarity) / len(keyword_similarity)

# Sort keywords by similarity scores
sorted_keywords = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)

# Print top N keywords
N = 10  # Number of top keywords to print
top_keywords = sorted_keywords[:N]
#subject
#lower case all subjects
#lowercase event, and check to see what subjects are in event
#print out subjects
print("Top keywords for tagging the event:")
for keyword, similarity in top_keywords:
    print(f"- {keyword}: {similarity}")


