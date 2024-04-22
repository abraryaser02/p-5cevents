import os
from openai import OpenAI
import json
import gensim
from gensim.models import Word2Vec
import re

import imaplib
import email
from email.header import decode_header
import time


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




def info_extraction(email):
  client = OpenAI(
      api_key=os.environ.get("OPENAI_API_KEY"),
  )

  #with open("/Users/sadhvinarayanan/Downloads/hivDist/openai-env/Chirps (1).txt", "rb") as f:
    #text = f.read().decode("utf-8")
  text = email
    #print(type(content))
    #name = text.split(":")[1].strip()

  #print(name)

  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=(
      {"role": "system", "content": "Here is some text about a school event you will have to analyze: " + text},
      {"role": "user", "content": "return ONLY a python dictionary, where the dictionary describes the event and has a key for the event name, description, date, location, start time, end time, contact information, and registration link if applicable. Please just give me the dictionary and no other text or symbols. Here are the keys you should use: event_name, description, date, location, start_time, end_time, contact_information, registration_link. I need the output to be a python dictionary so I can use it in my code directly."}
  )
  )
# {"role": "user", "content": "For each event, return a python dictionary which has elements for the event name, description, date, location, start time, end time (make sure to seperate start and end time as different elements), contact information (and the value for this key should be another list containing the contact person, email, and registration link). Do this for every event, dont cut it short. Also have it in python dict format. Don't put any text before the start of each dictionary, it should just be a list of dictionaries and nothing else. I want the first thing in the output to be the first dictionary. I want every event, nothign cut short."}

  final_str = completion.choices[0].message.content

#print(type(new_str))

  final_str = final_str.replace("python", "")
  final_str = final_str.replace("```", "")

#print(final_str)
  event_dict = eval(final_str)



  #print(type(str_dict))
  #print(list(event_dict.keys()))
  json_dict = json.dumps(event_dict, indent=4)

  return (json_dict)

  #print(json_dict)
  # event_name = event_dict["event_name"]
  # description = event_dict["description"]
  # date = event_dict["date"]
  # location = event_dict["location"]
  # start_time = event_dict["start_time"]
  # end_time = event_dict["end_time"]
  # contact_information = event_dict["contact_information"]
  # registration_link = event_dict["registration_link"]
  

    #ADD TO DATABASE HERE

def tagging(email): 
    # Load pre-trained Word2Vec model
    #word2vec_model = Word2Vec.load('path/to/pretrained/model')


    # Keywords for event tagging
    keywords = ['academic', 'humanities', 'fellowship', 'protest', 'social justice', 'workshop', 'seminar', 'conference', 'symposium', 'panel', 'lecture', 'workshop series', 'career fair', 'networking', 'cultural', 'social', 'club', 'volunteer', 'orientation', 'recruitment', 'sports', 'party', 'wellness']

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


    # Event description
    #event_description = "Fellowship Information Dinner @ Frank Blue Room, Wed, 3/20 from 5:15 - 6:15 PM What exactly is a fellowship? How do you apply for one? When can you apply for one? Get your answers to these questions from the CDO Fellowship Advisor Jason Jeffrey"
    #event_description = "Last Friday Claremont Police arrested 20 students at Pomona College who were conducting a sit-in, charging them with trespassing and obstruction of justice. Join Professors Shields and Kim for a discussion over this event's implications for student activism and institutional responses during Ath Tea at Adams Courtyard at the Athenaeum from 3 - 4:30 PM this Friday, April 12."
    event_description = email
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
        #print(event_description[i])
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
    N = 5  # Number of top keywords to print
    top_keywords = sorted_keywords[:N]
    #subject
    #lower case all subjects
    #lowercase event, and check to see what subjects are in event
    #print out subjects
    keyword_list = []
    #print("Top keywords for tagging the event:")
    for keyword, similarity in top_keywords:
        keyword_list.append(keyword)
        #print(f"- {keyword}: {similarity}")


    return(keyword_list, subject_list)




#print(tagging("hi"))

#print(info_extraction("email"))
  #print(final_list[0])



# Gmail IMAP server settings
gmail_user = "testing5c5cevents@gmail.com"
gmail_password = "gicn cpzd kkvg ealf"
def check_unread_emails():
    # Connect to the Gmail IMAP server
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    try:
        # Log in to your Gmail account
        mail.login(gmail_user, gmail_password)
        # Select the mailbox you want to access (e.g., 'inbox')
        mail.select("inbox")
        # Search for unread emails
        status, messages = mail.search(None, 'UNSEEN')
        # Get the list of email IDs
        mail_ids = messages[0].split()
        email_contents = []  # List to store email contents as strings
        for mail_id in mail_ids:
            status, msg_data = mail.fetch(mail_id, "(RFC822)")
            raw_email = msg_data[0][1]
            email_message = email.message_from_bytes(raw_email)
            email_content = ""
            subject, encoding = decode_header(email_message["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")
            email_content += f"Subject: {subject}\n"
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    email_content += "Body:\n" + body + "\n"
            email_contents.append(email_content)
        # Process the email contents
        for content in email_contents:
            json_dict = info_extraction(content)
            result = tagging(content)
            topic_tag = result[0]
            subject_tag = result[1]

            print(json_dict)
            print(topic_tag)
            print(subject_tag)

            #print(content)
    finally:
        # Logout from the mail server
        mail.logout()
# Schedule the function to run every 30 secs


while True:
    print("Checking for new emails...")
    check_unread_emails()
    print("Waiting for 30 secs...")
    time.sleep(30)  # Wait 30 secs





