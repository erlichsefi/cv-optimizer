
from llm_store import get_compliation,experience_chatbot
from filestore import get_completed_cv_data,get_cv_blueprint,get_position_data,set_position_cv_offers,set_position_cv_offer
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



def chat_loop():
    position_data = get_position_data()
    cv_data = get_completed_cv_data()
    cv_blueprint = get_cv_blueprint()


    def review_by_hiring_team(position_data,cv_data):

        prompt = f"""
        You are an experienced technical recruiter tasked with filling an open position in a leading tech company. 
        Your goal is to find the best candidate who not only possesses the necessary technical skills but 
        also fits well with the company culture.  Your Job is to give critical feedback on the CV you receive to the position.
        Be concise, professional, compare the lastast CV to the poisition and give feedback if something missing.

        The position you are hiring is:
        {json.dumps(position_data,indent=4)}

        The user CV:
        {json.dumps(cv_data,indent=4)}
        
        Provide all questions in the following format:

        ```json
        [
            {{
                "missmatch": "<the missmatch betwen the candiate CV and the the position>",
                "critical_level": "<HIGH,MID,LOW>",
                "question": "<the question to the user to learn if has an experince>",
            }}
            
            // more if you have
        ]
        ```
        """

        return get_compliation("",prompt,is_json_expected=True)


    def optimize_and_wonder(gaps_to_adresss,user_cv):
        prompt = f"""
        You are an independent HR recruiter, committed to referring the perfect candidate for the job. 
        You help candidates to optimize the CV for the position, optimize the CV.
        I've found the following mismatch, 
        issues to address:
        {json.dumps(gaps_to_adresss,indent=4)}

        user CV:
        {json.dumps(user_cv,indent=4)}
        reponse foramt:
        ```json
        {{
            "user_cv": {json.dumps(cv_blueprint,indent=4)}
            "missing_information": [
                // questions to ask to minimize the gap between the position requirement and the CV
            ]
        }}
        ```
        """
        return get_compliation("",prompt,is_json_expected=True)

    def complete_from_chat(user_cv,messages,expected):
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
    
    for index in range(2):
        gaps_to_adresss = review_by_hiring_team(position_data,cv_data)
        cv_and_wondering = optimize_and_wonder(gaps_to_adresss,cv_data)

        current_cv = cv_and_wondering['user_cv']
        set_position_cv_offer(current_cv,index)
        system_prompt = f"""
        You are an independent HR recruiter, committed to referring the perfect candidate for the job. 
        You help candidates to optimize the CV for the position, optimize the CV.
        you've already optimized the your CV to:
        {json.dumps(current_cv,indent=4)} 

        and have some question to adress:
        {json.dumps(cv_and_wondering['missing_information'],indent=4)}

        """
        

        messages = experience_chatbot(system_prompt,topic="understanding the cv")
        cv_data = complete_from_chat(cv_data,messages,cv_blueprint)


def multi_agents():
    logging_session_id = autogen.runtime_logging.start(config={"dbname": "logs.db"})

    position_data = get_position_data()
    cv_data = get_completed_cv_data()
    cv_blueprint = get_cv_blueprint()
    llm_config = {
            "config_list": [{"model": "gpt-3.5-turbo", "api_key": os.environ['OPENAI_API_KEY'], "cache_seed": 42}]
        }
    user_proxy = autogen.UserProxyAgent(
        name="User_proxy",
        description="The User that would like to submit it's CV",
        system_message=f"""You are looking to get an interview, your CV is:
        {json.dumps(cv_data,indent=4)}
        """,
        human_input_mode="ALWAYS"
    )
    recriter = autogen.AssistantAgent(
        name="Hiring_technical_recruiter",
        description="an technical recruiter in the hiring compeny",
        system_message=f"""
        You are an experienced technical recruiter tasked with filling an open position in a leading tech company. 
        Your goal is to find the best candidate who not only possesses the necessary technical skills but 
        also fits well with the company culture.  Your Job is to give critical feedback of the CV you recive to the poistion.
        Be concise, professional, and engaging in your communication.

        The position your are hiring is:
        {json.dumps(position_data,indent=4)}
        """,
        llm_config=llm_config
    )
    technical_recriter = autogen.AssistantAgent(
        name="External_recruiter",
        description="external HR recruite that will help me get the position",
        system_message=f"""
        You are independent HR recruiter, committed to refer the perfect candidate for the job. 
        You help candidtes optimize their CV, you iteratively:
          - optimize the CV to the position
          - ask the hiring team for feedback
          - ask the user for more inforamtion that can improve the user CV.
          - and try again.
       
        CV must be in the following format:
        {json.dumps(cv_blueprint,indent=4)}
        """,
        llm_config=llm_config
    )
    os.environ['WAY'] = "Hiring_technical_recruiter"
    def allowlist(last_speaker: autogen.Agent, groupchat: autogen.GroupChat):
        if last_speaker.name == "User_proxy":
            return list(filter(lambda x: x.name == "External_recruiter",groupchat.agents))[0]
        elif last_speaker.name == "Hiring_technical_recruiter":
            return list(filter(lambda x: x.name == "External_recruiter",groupchat.agents))[0]
        elif last_speaker.name == "External_recruiter":
            agent =  list(filter(lambda x: x.name == os.environ['WAY'],groupchat.agents))[0]
            os.environ['WAY'] = "User_proxy" if os.environ['WAY'] == "Hiring_technical_recruiter" else "External_recruiter"
            return agent
        else:
            raise ValueError()


    recriter_groupchat = autogen.GroupChat(agents=[user_proxy, recriter, technical_recriter], messages=[], max_round=12,
                                       speaker_selection_method=allowlist)
    manager = autogen.GroupChatManager(groupchat=recriter_groupchat, llm_config=llm_config)
    
    result = user_proxy.initiate_chat(
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

    autogen.runtime_logging.stop()


    result
if __name__ == "__main__":
    chat_loop()




   











