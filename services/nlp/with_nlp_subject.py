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
#word2vec_model = Word2Vec.load('path/to/pretrained/model')


# Keywords for event tagging
keywords = ['academic', 'humanities', 'fellowship', 'protest', 'social justice', 'workshop', 'seminar', 'conference', 'symposium', 'panel', 'lecture', 'workshop series', 'career fair', 'networking', 'cultural', 'social', 'club', 'volunteer', 'orientation', 'recruitment', 'sports', 'party', 'wellness']
subjects = [
'computer', 'physics', 'biology', 'chemistry',
'math', 'humanities and social sciences', 'literature', 'history',
'business', 'economics']
#keywords = ['computer science', 'machine learning', 'physics', 'biology', 'art', 'chemistry'business','economics']

cs_words = {
    "computer science", "algorithm", "data structure", "programming", "coding", "software", "optimization",
    "hardware", "networking", "database", "cybersecurity", "artificial intelligence", 
    "machine learning", "deep learning", "natural language processing", "computer vision", 
    "web development", "mobile development", "operating system", "cloud computing", 
    "parallel computing", "computer graphics", "human-computer interaction", 
    "computer architecture", "internet of things", "big data", "data mining", 
    "computer science", "algorithmic complexity", "software engineering", 
    "computer programming", "computer engineering", "digital logic", "computational theory", 
    "computer vision", "computer network", "computer security", "computer software", 
    "computer hardware", "computer system", "computer algorithm", "computer application", 
    "computer software", "computer programmer", "computer technology", "computer simulation"
}

physics_words = {
    "mechanics", "thermodynamics", "electromagnetism", "optics", "quantum",
    "relativity", "kinematics", "dynamics", "statics", "fluids"
}

biology_words = {
    "biology", "evolution", "genetics", "mutation", "inheritance", "adaptation", "ecology", 
    "biotechnology", "microbiology", "physiology", "anatomy", "taxonomy"
}

chemistry_words = {
    "chemistry", "experiment", "laboratory", "research", "analysis",
    "chemical", "reaction", "molecule", "atom", "element",
    "compound", "bond", "stoichiometry", "acid", "base",
    "solution", "equilibrium", "kinetics", "thermodynamics", 
    "oxidation", "reduction", "catalyst", "periodic table", 
    "bonding", "organic", "inorganic", "physical chemistry"
}

humanities_social_sciences_words = {
    "humanities", "social sciences", "history", "literature", 
    "philosophy", "sociology", "psychology", "anthropology",
    "economics", "political science", "linguistics", "archaeology",
    "cultural studies", "geography", "law", "education",
    "communication studies", "media studies", "ethnic studies",
    "gender studies", "religious studies", "demography",
    "urban studies", "development studies", "library science"
}

literature_words = {
    "literature", "novel", "poetry", "fiction", 
    "prose", "drama", "play", "author",
    "writing", "poet", "story", "verse",
    "literary", "narrative", "theme", "plot",
    "character", "setting", "symbolism", "metaphor",
    "imagery", "rhyme", "meter", "genre",
    "criticism", "analysis", "interpretation", "classic"
}

economics_words = {
    "economics", "economic", "finance", "macroeconomics", 
    "microeconomics", "market", "trade", "business", 
    "policy", "investment", "capital", "monetary", 
    "fiscal", "banking", "development", "growth", 
    "employment", "income", "inflation", "deflation", 
    "supply", "demand", "market", "cost", 
    "price", "supply chain", "management", "strategy"
}

business_words = {
    "business", "management", "leadership", 
    "entrepreneurship", "startup", "enterprise", 
    "industry", "commerce", "marketing", 
    "sales", "finance", "strategy", 
    "innovation", "operation", "supply chain", 
    "logistics", "organization", "administration", 
    "consulting", "investment", "corporate", 
    "executive", "venture", "globalization", 
    "entrepreneur", "manager", "CEO", 
    "director", "analyst"
}

math_words = {
    "mathematics", "math", "algebra", 
    "geometry", "calculus", "statistics", 
    "probability", "analysis", "number theory", 
    "logic", "combinatorics", "topology", 
    "differential equations", "linear algebra", 
    "optimization", "numerical analysis", "graph theory", 
    "mathematical modeling", "mathematical physics", 
    "mathematical biology", "mathematical finance", 
    "mathematical logic", "mathematical programming", 
    "mathematical economics", "applied mathematics", 
    "pure mathematics", "discrete mathematics", 
    "complex analysis", "game theory"
}


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


subjects_embeddings = {}
final_subject = []
for subject in subjects:
    subject_tokens = [subject] #subject.split()   Tokenize the keyword if it contains multiple words
    subject_embedding = []
    for token in subject_tokens:
        print(token)
        if token in word2vec_model.wv.key_to_index:
            print("hi")
            subject_embedding.append(word2vec_model.wv.get_vector(token))
    if subject_embedding:
        subjects_embeddings[subject] = sum(subject_embedding) / len(subject_embedding)
print(subjects_embeddings)

# Event description
#event_description = "Fellowship Information Dinner @ Frank Blue Room, Wed, 3/20 from 5:15 - 6:15 PM What exactly is a fellowship? How do you apply for one? When can you apply for one? Get your answers to these questions from the CDO Fellowship Advisor Jason Jeffrey"
#event_description = "Last Friday Claremont Police arrested 20 students at Pomona College who were conducting a sit-in, charging them with trespassing and obstruction of justice. Join Professors Shields and Kim for a discussion over this event's implications for student activism and institutional responses during Ath Tea at Adams Courtyard at the Athenaeum from 3 - 4:30 PM this Friday, April 12."
event_description = "Join us for a dynamic conference showcasing innovations in chemistry. Discover sustainable approaches to chemical synthesis, reaction optimization, and waste minimization. Learn about the principles of green chemistry and their application in designing environmentally benign processes. Engage with experts, industry leaders, and researchers to explore the future of sustainable chemistry."
# Preprocess the event description

#remove punctuation
event_description = re.sub('[^a-zA-Z]', ' ', event_description)

#remove tags
event_description=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",event_description)

#remove digits and special chars
event_description=re.sub("(\\d|\\W)+"," ",event_description)
event_description = event_description.lower().split()
event_description.append("stop") # extra buffer for for loop below

subject_list = set()
for i in range (len(event_description) - 1):
    print(event_description[i])
    if ((event_description[i] in cs_words) or str(event_description[i] + " " + event_description[i+1]) in cs_words):
        subject_list.add("Computer Science")
    if ((event_description[i] in economics_words) or str(event_description[i] + " " + event_description[i+1]) in economics_words):
        subject_list.add("Economics")
    if ((event_description[i] in physics_words) or str(event_description[i] + " " + event_description[i+1]) in physics_words):
        subject_list.add("Physics")
    if ((event_description[i] in biology_words) or str(event_description[i] + " " + event_description[i+1]) in biology_words):
        subject_list.add("Biology")
    if ((event_description[i] in chemistry_words) or str(event_description[i] + " " + event_description[i+1]) in chemistry_words):
        subject_list.add("Chemistry")
    if ((event_description[i] in humanities_social_sciences_words) or str(event_description[i] + " " + event_description[i+1]) in humanities_social_sciences_words):
        subject_list.add("Humanities and Social Science")
    if ((event_description[i] in math_words) or str(event_description[i] + " " + event_description[i+1]) in math_words):
        subject_list.add("Math")
    if ((event_description[i] in business_words) or str(event_description[i] + " " + event_description[i+1]) in business_words):
        subject_list.add("Business")
    if ((event_description[i] in literature_words) or str(event_description[i] + " " + event_description[i+1]) in literature_words):
        subject_list.add("Literature")
        



# Calculate similarity between event description and each keyword
similarity_scores_keyword = {}
for keyword, embedding in keyword_embeddings.items():
    keyword_similarity = []
    for word in event_description:
        if word in word2vec_model.wv.key_to_index:
            word_embedding = word2vec_model.wv.get_vector(word)
            similarity = word2vec_model.wv.cosine_similarities(embedding, [word_embedding])
            keyword_similarity.append(max(similarity))
    if keyword_similarity:
        similarity_scores_keyword[keyword] = sum(keyword_similarity) / len(keyword_similarity)

# Sort keywords by similarity scores
sorted_keywords = sorted(similarity_scores_keyword.items(), key=lambda x: x[1], reverse=True)

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


similarity_scores_subject = {}
for subject, embedding in subjects_embeddings.items():
    print("jo")
    keyword_similarity = []
    for word in event_description:
        if word in word2vec_model.wv.key_to_index:
            word_embedding = word2vec_model.wv.get_vector(word)
            print(subject, word)
            similarity = word2vec_model.wv.cosine_similarities(embedding, [word_embedding])
            print(similarity)
            keyword_similarity.append(max(similarity))
    if keyword_similarity:
        similarity_scores_subject[subject] = sum(keyword_similarity) / len(keyword_similarity)

sorted_keywords_subject = sorted(similarity_scores_subject.items(), key=lambda x: x[1], reverse=True)
# Print top N subjects
N = 5  # Number of top keywords to print
top_keywords_subject = sorted_keywords_subject[:N]
#subject
#lower case all subjects
#lowercase event, and check to see what subjects are in event
#print out subjects
print("Top subjects for tagging the event:")
for keyword, similarity in top_keywords_subject:
    print(f"- {keyword}: {similarity}")

print(subject_list)