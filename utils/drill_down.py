import json
import os
from enum import Enum
from openai import OpenAI
import retry

from chat_on_topic import chatbot

def get_user_cv(user_cv_json_path):
    with open(user_cv_json_path,'r') as file:
        return json.load(file)

def get_expected_cv_data(user_json_filename):
    with open(user_json_filename, "r") as file:
        return json.load(file)
    
def set_user_cv(output_user_csv,user_cv):
    with open(output_user_csv,"w") as file:
        json.dump(user_cv,file)

def get_compliation(system_message, user_input, api_key=None):
    if not api_key:
        api_key = os.environ['OPENAI_API_KEY']

    client = OpenAI(api_key=api_key)
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input},
        ],
        stream=False,
    )
    return stream

@retry.retry(exceptions=(json.decoder.JSONDecodeError))
def get_questions(user_cv):

    prompt = f"""
    Your goal is to complete the information missing or corrupted user data.
    For each entry in the user data, make sure the value stored make sense, or not missing, if it missing provide a question addressed to the user from which you can learn what the correct value to place there.

    user data:
    {json.dumps(user_cv,indent=4)}

    Provide all questions in the following format:

    ```json
    [{{
        "question":"<the question to the user>",
        "regex":"<a python regex to validate the user input>",
        "regex_fail_message":"<the message if the regex fail>",
        "target_missing": [a list of path 'key' and indexies only from the root of the json to the place to put the value]
    }},
    // more if you have
    ]
    ```
    When you don't have any other question respond with 'quit'.
    """

    response = get_compliation("",prompt)
    return json.loads(response.choices[0].message.content.replace("```json","").replace("```",""))
    


def chat_on_section(section,section_title):
    system_prompt = f"""
        You are interviewing me about this period in my life:
        {json.dumps(section,indent=4)}
        You Goal is to asses what skills I've gained during this time.
        When you think that you've understood the skill set I've gained you can respond with 'quit'.


        user data:
        {json.dumps(section,indent=4)}

        
    """

    return chatbot(system_prompt,topic=section_title)
    



def run(user_cs_json_path):
    user_cv = get_user_cv(user_cs_json_path)

    # this is UI component.
    drill_down_sections = {
        'education':lambda x: f"study to a {x['degree']} in {x['institution']}",
        'publications':lambda x: f"publications of '{x['title']}'",
        'projects':lambda x: f"project at {x['title']}",
        'experience':lambda x: f"time in {x['company']} as \'{x['title']}\'",
        
    }
    # TODO: sort exection by start_date
    for section,callout in drill_down_sections.items():
        
        for index,entry in enumerate(user_cv[section]):
            section_title = callout(entry)
            messages = chat_on_section(entry, section_title=section_title)

            with open(f"user_data/{section}_{index}.json",'w') as file:
                json.dump(messages,file)
    

    


if __name__ == "__main__":
    run("user_data/full_user_cv.json")