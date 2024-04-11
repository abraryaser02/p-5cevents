import os
from openai import OpenAI
import json

def func():
  client = OpenAI(
      api_key=os.environ.get("OPENAI_API_KEY"),
  )

  with open("/Users/sadhvinarayanan/Downloads/hivDist/openai-env/Chirps (1).txt", "rb") as f:
    text = f.read().decode("utf-8")
    #print(type(content))
    #name = text.split(":")[1].strip()

  #print(name)

  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=(
      {"role": "system", "content": "Here is some text about many school events you will have to analyze: " + text},
      {"role": "user", "content": "return ONLY a python list of dictionaries, where each dictionary describes each event and has a key for the event name, description, date, location, start time, end time, contact information, and registration link if applicable. Please just give me the list and no other text or symbols. Here are the keys you should use: event_name, description, date, location, start_time, end_time, contact_information, registration_link. I need the output to be a python list so I can use it in my code directly. And do all the events, I need all of them in the final list."}
  )
  )
# {"role": "user", "content": "For each event, return a python dictionary which has elements for the event name, description, date, location, start time, end time (make sure to seperate start and end time as different elements), contact information (and the value for this key should be another list containing the contact person, email, and registration link). Do this for every event, dont cut it short. Also have it in python dict format. Don't put any text before the start of each dictionary, it should just be a list of dictionaries and nothing else. I want the first thing in the output to be the first dictionary. I want every event, nothign cut short."}

  final_str = completion.choices[0].message.content

  return final_str

new_str = func()

#print(type(new_str))

final_str = new_str.replace("python", "")
final_str = final_str.replace("```", "")

#print(final_str)
final_list = eval(final_str)


for event_dict in final_list:
  #print(type(str_dict))
  #print(list(event_dict.keys()))
  json_dict = json.dumps(event_dict, indent=4)
  #print(json_dict)
  event_name = event_dict["event_name"]
  description = event_dict["description"]
  date = event_dict["date"]
  location = event_dict["location"]
  start_time = event_dict["start_time"]
  end_time = event_dict["end_time"]
  contact_information = event_dict["contact_information"]
  registration_link = event_dict["registration_link"]
  print(event_name)

  #ADD TO DATABASE HERE



#print(final_list[0])



