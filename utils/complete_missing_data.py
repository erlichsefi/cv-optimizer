import json
import re
import os
from enum import Enum
from openai import OpenAI
import retry

from llm_store import chatbot
from filestore import get_user_extract_cv_data,set_completed_cv_data,get_cv_blueprint

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



def set_value_at_xpath(current, xpath, value):
    for step in xpath[:-1]:
        if isinstance(current, list):
            current = current[step]
        elif isinstance(current, dict):
            current = current.get(step)
            if current is None:
                return
        else:
            return
    if isinstance(current, list):
        try:
            current[xpath[-1]] = value
        except IndexError:
            return
    elif isinstance(current, dict):
        current[xpath[-1]] = value



def validate_regex(regex, string):
    try:
        re.compile(regex)
        match = re.search(regex, string)
        if match:
            return True
        else:
            return False
    except re.error:
        return False


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
    


def complete_by_qna(user_cv):
    question_to_ask = get_questions(user_cv)
    for entry in question_to_ask:
        while True:
            print(f"Q: {entry['question']}")
            answer = input()
            if validate_regex(entry['regex'],answer):
                set_value_at_xpath(user_cv,entry['target_missing'],answer)
                break
            else:
                print(entry['regex_fail_message'])


def chat_on_question(user_cv):
    system_prompt = f"""
        Your goal is to complete the information missing or corrupted user data.
        For each entry in the user data, make sure the value stored make sense:
         - is it missing? if it missing provide a question addressed to the user from which you can learn what the correct value to place there.
         - is it corrupted? is the data there make correpted? if it mising provide a question that will verfiy the true value 

        user data:
        {json.dumps(user_cv,indent=4)}

        
    """

    messages = chatbot(system_prompt,topic="understanding the cv")
    
    expected = get_cv_blueprint()
    final_call = f"""
    You've interviewd a user about his cv in means to complete the information missing or corrupted user data.

    iterview:
    {json.dumps(messages,indent=4)}

    user data:
    {json.dumps(user_cv,indent=4)}

    emend the user data according to the information in the interview:
    1. include all the information from the user data.
    2. emend the infromation according to the information provided in the interview.
    
    ```json
    {json.dumps(expected,indent=4)}
    ```
    """
    response = get_compliation("",final_call)
    return json.loads(response.choices[0].message.content.replace("```json","").replace("```",""))




class How(Enum):
    QNA = complete_by_qna
    CHAT = chat_on_question

def run(how):
    user_cv = get_user_extract_cv_data()

    # this is UI component.
    emended_user_cv = how(user_cv)

    set_completed_cv_data(emended_user_cv)

    


if __name__ == "__main__":
    run(how=How.CHAT)