
from llm_store import get_compliation
from filestore import get_completed_cv_data,get_cv_blueprint,get_position_data,set_position_cv_offers
import json
import os
import autogen



def single_prompt_call():
    position_data = get_position_data()
    cv_data = get_completed_cv_data()
    cv_blueprint = get_cv_blueprint()

    offers = get_compliation(system_message="",user_input=f"""Task Description:
    You are tasked with optimizing a user's CV based on a given position description without revealing that the CV has been optimized or inventing information not present in the original CV.

    User CV:
    {json.dumps(cv_data,indent=4)}
                            
    Position Description:
    {json.dumps(position_data,indent=4)}
                            
    Instructions:

    - Review the user's CV carefully.
    - Analyze the position description to understand the specific requirements and preferences of the role.
    - Enhance the user's CV by rephrasing, restructuring, or emphasizing existing information to better match the position description.
    - Ensure that any modifications made are subtle and do not give away the fact that the CV has been optimized.
    - Avoid inventing new information or embellishing existing details beyond what is provided in the original CV.

    Additional Guidance:

    - Focus on highlighting relevant experiences, skills, and achievements that directly correlate with the position requirements.
    - Use language that mirrors the tone and terminology used in the position description.
    - Maintain the overall format and style of the original CV to avoid suspicion of tampering.

    Outcome:
    - Your final output should be an optimized version of the user's CV that appears natural and cohesive while effectively addressing the expectations outlined in the position description.
    - Provide the response in markdown.

    Response format:
    ```json
    {json.dumps(cv_blueprint,indent=4)}
    ```
    """,
    is_json_expected=True,
    num_of_gen=2,
    temperature=0.1
    )
    set_position_cv_offers(offers)

def multi_agents():
    position_data = get_position_data()
    cv_data = get_completed_cv_data()
    cv_blueprint = get_cv_blueprint()
    llm_config = {
            # "request_timeout": 600,
            "config_list": [{"model": "gpt-3.5-turbo", "api_key": os.environ['OPENAI_API_KEY'], "cache_seed": 42}]
        }
    user_proxy = autogen.UserProxyAgent(
        name="User_proxy",
        description="User that would like to submit it's CV",
        system_message=f"""You are looking to get an interview, your CV is:
        {json.dumps(cv_data,indent=4)}
        """,
        human_input_mode="ALWAYS"
    )
    recriter = autogen.AssistantAgent(
        name="Recruiter",
        description="an recruiter in the hiring compeny",
        system_message=f"""You are recruiter need to recruite the right person to the following position:
        {json.dumps(position_data,indent=4)}

        you need to examin issue that can prevent the user from geting the position.
        rememmber! you need to recruite to right person!
        """,
        llm_config=llm_config
    )
    technical_recriter = autogen.AssistantAgent(
        name="Technical_recruiter",
        description="Technical recriter that will help me get the position",
        system_message=f"""
        Your need to understand how to adjust the user CV to make it more likely it will get an interview,
        the user you would like to help getting the postion is:
        {json.dumps(cv_data,indent=4)}

        Your goal is to understand what to user can change in the CV.
        
        keep making varitaions on the CV and update it, the final foramt should be:
        {json.dumps(cv_blueprint,indent=4)}
        """,
        llm_config=llm_config
    )
    groupchat = autogen.GroupChat(agents=[recriter, technical_recriter,user_proxy], messages=[], max_round=12)
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)
    user_proxy.initiate_chat(
    manager, message=f"""Hey there,
    I've come across this amazing job opportunity that I'm really excited about, and I want to make sure my CV is perfectly tailored to it. I've attached the job description below so you can get a sense of what they're looking for.

    Could you please review my CV and make any necessary adjustments to better align it with the job description? I want to make sure I highlight the relevant skills and experiences without making it obvious that I've optimized it. 
    Also, please make sure not to add any information that isn't already in my CV.

    Thanks so much for your help, I really appreciate it!
    My CV:
    {json.dumps(cv_data,indent=4)}
                            
    Position Description:
    {json.dumps(position_data,indent=4)}

        
    """
    )
if __name__ == "__main__":
    multi_agents()




   











