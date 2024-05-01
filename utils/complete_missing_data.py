import json
import re
from .interface import TerminalInterface,UserInterface
from .llm_store import experience_chatbot,get_compliation
from .filestore import get_user_extract_cv_data,set_completed_cv_data,get_cv_blueprint,has_completed_cv_data




def get_questions(user_cv):

    prompt = f"""
    Your goal is to complete the information missing or corrupted user data.
    For each entry in the user data, make sure the value stored make sense, or not missing, if it missing provide a question addressed to the user from which you can learn what the correct value to place there.

    - resolve any unicode issue

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

    return get_compliation("",prompt,is_json_expected=True)
    
def get_issues_need_to_be_adressed(user_cv):

    prompt = f"""
    Your goal is to complete the information missing or corrupted in the user data.
    For all values (included nested ones) in the user data:
        - is the value missing? if it missing provide a question addressed to the user from which you can learn what the correct value to place there.
        - is the value corrupted? is the data there is correpted? if it corrupted provide a question that will verfiy the true value.
        - is the value make sense given the key? if not, verify it with the user. 

    user data:
    {json.dumps(user_cv,indent=4)}

    
    Provide all questions in the following format:

    ```json
    [
    "<the question to the user>",
    // more if you have
    ]
    ```
    """

    return get_compliation("",prompt,is_json_expected=True)


def complete_by_qna(user_cv,user_interface:UserInterface):
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
    
    question_to_ask = get_questions(user_cv)
    for entry in question_to_ask:
        while True:
            user_interface.send_user_message(f"{entry['question']}")
            answer = user_interface.get_user_input()
            if validate_regex(entry['regex'],answer):
                set_value_at_xpath(user_cv,entry['target_missing'],answer)
                break
            else:
                print(entry['regex_fail_message'])


def chat_on_question(user_cv,terminal_interface:UserInterface):
    issues_to_adresss = get_issues_need_to_be_adressed(user_cv)

    system_prompt = f"""
        Your goal is to complete the information missing or corrupted user data.

        user data:
        {json.dumps(user_cv,indent=4)}

        issues to address:
        {json.dumps(issues_to_adresss,indent=4)}
    """

    messages = experience_chatbot(system_prompt,terminal_interface, topic="validating what we got")
    
    expected = get_cv_blueprint()
    final_call = f"""
    You've interviewd a user about his cv in means to complete the information missing or corrupted in the user data.

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
    return get_compliation("",final_call,is_json_expected=True)



def run(terminal_interface:UserInterface):
    if not has_completed_cv_data():
        user_cv = get_user_extract_cv_data()

        # complete_by_qna
        emended_user_cv = chat_on_question(user_cv,terminal_interface)

        set_completed_cv_data(emended_user_cv)

        terminal_interface.send_user_message("We got it! Thanks!")
        terminal_interface.send_user_message("Moving on...")

    


if __name__ == "__main__":
    terminal_interface = TerminalInterface()
    run(terminal_interface)