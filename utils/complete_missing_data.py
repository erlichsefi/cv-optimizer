import json
import re
import os
from openai import OpenAI
import retry

def get_user_cv(user_cv_json_path):
    with open(user_cv_json_path,'r') as file:
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
    Your goal is to complete the information missing in the user data.
    Provide questions to resolve missing data, user data is:

    {json.dumps(user_cv,indent=4)}

    Provide all questions in the following format:

    ```json
    [{{
        "question":"<the question to the user>",
        "regex":"<a python regex to validate the user input>",
        "regex_fail_message":"<the message if the regex fail>",
        "target_missing": [xpath from the root of the json to the key in a list]
    }},
    // more if you have
    ]
    ```

    """

    response = get_compliation("",prompt)
    return json.loads(response.choices[0].message.content.replace("```json","").replace("```",""))
    


def run(user_cs_json_path,output_user_csv):
    user_cv = get_user_cv(user_cs_json_path)
    question_to_ask = get_questions(user_cv)
    
    # this is UI component.
    for entry in question_to_ask:

        while True:
            print(f"Q: {entry['question']}")
            answer = input()
            if validate_regex(entry['regex'],answer):
                set_value_at_xpath(user_cv,entry['target_missing'],answer)
                break
            else:
                print(entry['regex_fail_message'])

    set_user_cv(output_user_csv,user_cv)

    


if __name__ == "__main__":
    run("user_cv.json",output_user_csv="full_user_cv.json")