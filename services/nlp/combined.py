import os
import json
import re
import pickle
import imaplib
import email
from email.header import decode_header
import time
import subprocess
from openai import OpenAI
from gensim.models import Word2Vec

# Define the path to the model data pickle file for tagging
MODEL_DATA_PATH = 'path_to_model_data.pkl'

# Load Model 1 for event tagging
class TrainedEventsTagger:
    def __init__(self, pkl_file):
        with open(pkl_file, 'rb') as f:
            self.model_data = pickle.load(f)
        self.keyword_embeddings = self.model_data['keyword_embeddings']
        self.word_vectors = self.model_data['word_vectors']

    def tag(self, event_description):
        # Simplified tagging function for demonstration
        return ["tag1", "tag2", "tag3"]

# Function to clean and preprocess text
def clean_text(text):
    text = text.lower()
    text = re.sub('[^a-z]', ' ', text)
    return text.strip()

# Function to extract event data using OpenAI's GPT-3.5
def extract_event_data(email_content):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Extract structured event data."},
            {"role": "user", "content": email_content}
        ]
    )
    return completion.choices[0].message.content

# Function to update the database
def update_database(event_data):
    curl_command = f'curl -X POST http://localhost:5001/create_scraped_event -H "Content-Type: application/json" -d \'{json.dumps(event_data)}\''
    subprocess.run(curl_command, shell=True)

# Process each email content
def process_email(email_content):
    cleaned_content = clean_text(email_content)
    event_data = json.loads(extract_event_data(cleaned_content))
    tagger = TrainedEventsTagger(MODEL_DATA_PATH)
    tags = tagger.tag(event_data['description'])
    event_data['tags'] = tags
    update_database(event_data)

# Check for unread emails and process them
def check_unread_emails():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login("your_email@gmail.com", "your_password")
    mail.select("inbox")
    _, messages = mail.search(None, 'UNSEEN')
    for mail_id in messages[0].split():
        _, msg_data = mail.fetch(mail_id, "(RFC822)")
        raw_email = msg_data[0][1]
        email_message = email.message_from_bytes(raw_email)
        email_content = ""
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                email_content += part.get_payload(decode=True).decode()
        process_email(email_content)
    mail.logout()

# Main function to continuously check emails
def main():
    while True:
        print("Checking for new emails...")
        check_unread_emails()
        print("Waiting for 10 seconds...")
        time.sleep(10)

if __name__ == "__main__":
    main()
