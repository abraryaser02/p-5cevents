from gensim.models import Word2Vec
import gensim
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

paragraph = "Goal motivation & Free snacks with Pomona Sagefellows! Stop by our table at the SCC this Friday (3/22) between 11am-1pm for free snacks & goal-setting resources. Come add your goals to a community board & celebrate the semester. Queer Student Testimonies - Claremont Christian Fellowship Everyone is welcome at Friday Fellowship this week as we hear from some of our queer members about how their faith and sexuality have intersected. Doms Lounge 3/22 at 7pm. Free tacos after the meeting! Walker Flea Market & Free Boba from 5C Plant-Based! Buy homemade, student-created items from 5C students at the Walker Flea Market on Friday, March 22 from 4-7pm at Walker Beach. Items sold will include clothes, crochet creations, handmade jewelry, and art prints. Practice sustainability by enjoying a plant milk-based boba in a reusable cup paid for by the Pomona EcoReps! Psychology Research Study Participation for Credit and/or Raffle Entry Participate in my online senior thesis study on young adults' experiences of spending time alone! Earn 0.5 research participation credits if eligible and be entered into a raffle to receive one of three $40 VISA gift cards. And, spend some time reflecting on the alone-time in your life! The survey only takes about 20 minutes. If you would like to participate, click the link below to access the survey. https://pitzer.co1.qualtrics.com/jfe/form/SV_8jlGJrL1uY3YwNE Thank you! The Pomona Student Union Presents... What Is College For? Um... Why are we here? What are we doing? What is this all for, really? Join Professor Susan McWilliams Barndt, Professor Guillermo Douglass-Jaimes, & Professor Stef Torralba for a critical discussion of the purpose of college. Possible topics include the role of the liberal arts college, elitism & diversity, organizing & the classroom, and more. When: Thursday, March 21st, at 7:00 PM in Edmunds Ballroom Perks: Free (Sunright!) boba and Caylor's cookies"

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
keywords = ['academic', 'fellowship', 'workshop', 'seminar', 'conference', 'symposium', 'panel discussion', 'lecture', 'workshop series', 'career fair', 'networking', 'cultural event', 'social event', 'club meeting', 'volunteer opportunity', 'orientation', 'recruitment', 'sports event', 'fundraising', 'celebration', 'health & wellness']

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
event_description = "Fellowship Information Dinner @ Frank Blue Room, Wed, 3/20 from 5:15 - 6:15 PM What exactly is a fellowship? How do you apply for one? When can you apply for one? Get your answers to these questions from the CDO Fellowship Advisor Jason Jeffrey"

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
N = 5  # Number of top keywords to print
top_keywords = sorted_keywords[:N]
print("Top keywords for tagging the event:")
for keyword, similarity in top_keywords:
    print(f"- {keyword}: {similarity}")


