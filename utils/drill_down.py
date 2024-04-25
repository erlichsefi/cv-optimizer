import json
import retry
from filestore import get_completed_cv_data,set_drill_down_communiation
from llm_store import get_compliation,chatbot



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
    



def run():
    user_cv = get_completed_cv_data()

    # this is UI component.
    drill_down_sections = {
        'education':lambda x: f"study to a {x['degree']} in {x['institution']}",
        'publications':lambda x: f"publications of '{x['title']}'",
        'projects':lambda x: f"project at {x['title']}",
        'experience':lambda x: f"time in {x['company']} as \'{x['title']}\'",
        
    }
    # TODO: sort exection by start_date
    user_cv_message = dict()
    for section,callout in drill_down_sections.items():
        
        section_message = list()
        for entry in user_cv[section]:
            section_title = callout(entry)
            messages = chat_on_section(entry, section_title=section_title)
            section_message.append(messages)

        user_cv_message[section] = section_message

    set_drill_down_communiation()


    


if __name__ == "__main__":
    run()