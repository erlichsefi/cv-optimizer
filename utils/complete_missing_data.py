import json
import re
from .interface import TerminalInterface, UserInterface
from .llm_store import experience_chatbot, get_compliation


def get_issues_need_to_be_adressed(user_interface: UserInterface):
    user_cv = user_interface.get_user_extract_cv_data()
    
    prompt = f"""
    Your goal is to complete the information missing or corrupted in the user CV data.
    For all keys (included nested ones) in the user data, check:
        - is the value missing? if it missing provide a question addressed to the user from which you can learn what the correct value to place there.
        - is the value corrupted? is the data there is correpted? if it corrupted provide a question that will verfiy the true value.
        - is the value make sense given the key name? if not, verify it with the user. 

    But:
    - don't ask question 'to ensure the accuracy'

    user data:
    {json.dumps(user_cv,indent=4)}

    
    Provide all questions in the following format:

    ```json
    {{
        "possible_issue":[
            {{
                "xpath":"<the xpath to the value in question",
                "categoty":"<one of 'missing' or 'corrupted data' or 'value did not make sense given key'>",
                "issue":"<the value from the user data that seems to be an issue>",
                "reason":"<the reason you think the value is an issue"

            }}
            // more if you have
        ],
        "confirmed_question":[
        // a question on the issues in 'possible_issue' that seems ok.
        ]
    ]
    }}
    ```
    """

    issues_to_adresss = get_compliation("", prompt, is_json_expected=True)
    user_interface.set_issues_to_overcome(issues_to_adresss)


def summarize_chat_into_cv(user_interface: UserInterface, chat_id):
    messages = user_interface.get_chain_messages(chat_id)
    expected = user_interface.get_cv_blueprint()
    user_cv = user_interface.get_user_extract_cv_data()

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
    completed_cv = get_compliation("", final_call, is_json_expected=True)
    user_interface.set_completed_cv_data(completed_cv)


def chat_to_validate_extracted_cv(user_interface: UserInterface, id):
    issues_to_adresss = user_interface.get_issues_to_overcome()
    user_cv = user_interface.has_user_extract_cv_data()
    system_prompt = f"""
        Your goal is to complete the information missing or corrupted user data.

        user data:
        {json.dumps(user_cv,indent=4)}

        issues to address:
        {json.dumps(issues_to_adresss,indent=4)}
    """

    experience_chatbot(
        system_prompt, user_interface, id, topic="validating what we got from your CV"
    )


def chat_on_question(user_interface: UserInterface):
    """completed the user infomration by chat"""
    if not user_interface.has_issues_to_overcome():

        with user_interface.processing("Looking on what we got..."):
            get_issues_need_to_be_adressed(user_interface)
    #
    chat_id = "extracted_cv"
    if not user_interface.has_chain_messages(chat_id, closed=True):
        chat_to_validate_extracted_cv(user_interface, chat_id)
    #
    if (
        user_interface.has_chain_messages(chat_id, closed=True)
        and not user_interface.has_completed_cv_data()
    ):
        with user_interface.processing("Wraping up..."):
            summarize_chat_into_cv(user_interface, chat_id)
    #


# def run(user_interface:UserInterface):
#     user_cv = user_interface.get_user_extract_cv_data()

#     emended_user_cv = chat_on_question(user_cv,user_interface)

#     user_interface.set_completed_cv_data(emended_user_cv)


if __name__ == "__main__":
    terminal_interface = TerminalInterface()
    chat_on_question(terminal_interface)
