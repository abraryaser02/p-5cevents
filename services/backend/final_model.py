import os
from openai import OpenAI
import json
from datetime import datetime
import re
from TrainedEventsTagger import TrainedEventsTagger
import imaplib
import email
from email.header import decode_header
import time
import requests

# Define the function to parse time
def parse_time(time_str):
    try:
        return datetime.strptime(time_str, "%I:%M%p").isoformat()
    except ValueError:
        return None

# Define the function to extract event information
def info_extraction(email_content):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    text = email_content

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=(
            {"role": "system", "content": "Here is some text about a school event you will have to analyze: " + text},
            {"role": "user", "content": "return ONLY a python dictionary, where the dictionary describes the event and has a key for the event name, description, date, location, start time, end time, contact information, and registration link if applicable. Please just give me the dictionary and no other text or symbols. Here are the keys you should use: event_name, description, date, location, start_time, end_time, contact_information, registration_link. I need the output to be a python dictionary so I can use it in my code directly."}
        )
    )

    final_str = completion.choices[0].message.content

    final_str = final_str.replace("python", "")
    final_str = final_str.replace("```", "")

    event_dict = json.loads(final_str)
    print(event_dict)

    json_dict = json.dumps(event_dict, indent=4)

    return json_dict

# Instantiate the TrainedEventsTagger
tagger = TrainedEventsTagger('events_tagger_model_parameters_new.pkl')

# Gmail IMAP server settings
gmail_user = "testing5c5cevents@gmail.com"
gmail_password = "gicn cpzd kkvg ealf"

# Define the function to check unread emails
def check_unread_emails():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    try:
        mail.login(gmail_user, gmail_password)
        mail.select("inbox")
        status, messages = mail.search(None, 'UNSEEN')
        mail_ids = messages[0].split()
        email_contents = []

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
                    try:
                        body = part.get_payload(decode=True).decode('utf-8', 'ignore')
                        email_content += "Body:\n" + body + "\n"
                    except UnicodeDecodeError:
                        # Handle decoding errors
                        pass
            email_contents.append(email_content)

        for content in email_contents:
            client = OpenAI(
                api_key=os.environ.get("OPENAI_API_KEY"),
            )
            emails = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=(
                    {"role": "system", "content": "Here is some text about events you have to analyze, we want to extract individual events from it if it has many events" + content},
                    {"role": "user", "content": "please return a list of the different events, where each event is a string. Don't include any other symbols or text, I just want the python list so I can directly use it in my code"}
                )
            )

            final_str = emails.choices[0].message.content

            final_str = final_str.replace("python", "")
            final_str = final_str.replace("```", "")

            event_lists = json.loads(final_str)

            for event in event_lists:
                json_dict = info_extraction(event)
                tags = tagger.tag(event)
                data_dict = json.loads(json_dict)
                data_dict["tags"] = tags
                print(data_dict)
                execute_post_request(data_dict)
                

    finally:
        mail.logout()

def execute_post_request(data):
    # Extract data from the dictionary
    name = data['event_name']
    description = data['description']
    location = data['location']
    start_time = data.get('start_time', None)
    end_time = data.get('end_time', None)
    organization = ''  # Assuming the organization is not provided in the data dictionary
    contact_information = data['contact_information']
    registration_link = data['registration_link']
    keywords = data.get('tags', [])  # Get tags if available, otherwise an empty list

    # Convert specific time formats to datetime objects
    if start_time:
        start_time = parse_time(start_time)
    if end_time:
        end_time = parse_time(end_time)

    # Create the JSON payload
    payload = {
        "name": name,
        "description": description,
        "location": location,
        "start_time": start_time,
        "end_time": end_time,
        "organization": organization,
        "contact_information": contact_information,
        "registration_link": registration_link,
        "keywords": keywords
    }

    # Convert payload to JSON string
    json_payload = json.dumps(payload)

    # Send POST request
    url = 'http://backend:5000/create_event'
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json_payload)

    # Check response status
    if response.status_code == 200:
        print("Event created successfully.")
    else:
        print("Error creating event:", response.text)

# Main loop to continuously check for new emails
while True:
    print("Checking for new emails...")
    check_unread_emails()
    print("Waiting for 10 secs...")
    time.sleep(10)
