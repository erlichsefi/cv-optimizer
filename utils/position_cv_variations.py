from .llm_store import get_compliation, experience_chatbot
from .interface import TerminalInterface, UserInterface
import json
import os
import autogen


def single_prompt_call(user_interface):
    position_data = user_interface.get_position_data()
    cv_data = user_interface.get_completed_cv_data()
    cv_blueprint = user_interface.get_cv_blueprint()

    offers = get_compliation(
        system_message="",
        user_input=f"""Task Description:
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
        temperature=0.1,
    )
    user_interface.set_position_cv_offers(offers)


def review_by_hiring_team(user_interface: UserInterface, position_name:str = None):
    position_data = user_interface.get_position_data(position_name=position_name)
    cv_data = user_interface.get_completed_cv_data()

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

    gaps_to_adresss = get_compliation("", prompt, is_json_expected=True)
    gaps_to_adresss = user_interface.set_identified_gap_from_hiring_team(
        gaps_to_adresss
    )


def optimize_and_wonder(user_interface: UserInterface, gen_id):
    cv_data = user_interface.get_completed_cv_data()
    gaps_to_adresss = user_interface.get_identified_gap_from_hiring_team()
    cv_blueprint = user_interface.get_cv_blueprint()

    prompt = f"""
    You are an independent HR recruiter, committed to referring the perfect candidate for the job. 
    You help candidates to optimize the CV for the position, optimize the CV.
    I've found the following mismatch:
    {json.dumps(gaps_to_adresss,indent=4)}

    user CV:
    {json.dumps(cv_data,indent=4)}
    
    - emend the user cv so it may overcome those gaps.
    - be truthful.

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
    cv_and_wondering = get_compliation("", prompt, is_json_expected=True)
    user_interface.set_base_optimized(cv_and_wondering["user_cv"], gen_id)
    user_interface.set_issues_to_solve_in_chat(
        cv_and_wondering["missing_information"], gen_id
    )


def create_n_optimzied_variation(user_interface: UserInterface, n=2, position_name:str = None):
    cv_data = user_interface.get_completed_cv_data()
    gaps_to_adresss = user_interface.get_identified_gap_from_hiring_team()
    cv_blueprint = user_interface.get_cv_blueprint()

    prompt = f"""
    You are an independent HR recruiter, committed to referring the perfect candidate for the job. 
    You help candidates to optimize the CV for the position, optimize the CV.
    I've found the following mismatch:
    {json.dumps(gaps_to_adresss,indent=4)}

    user CV:
    {json.dumps(cv_data,indent=4)}
    
    - emend the user cv so it may overcome those gaps.
    - be truthful.

    reponse foramt:
    ```json
    {json.dumps(cv_blueprint,indent=4)}
    ```
    """
    variations = get_compliation("", prompt, is_json_expected=True, num_of_gen=n)
    user_interface.set_position_cv_offers(variations,position_name)


def enrich_from_chat(user_interface: UserInterface, chat_id, gen_id):
    cv_blueprint = user_interface.get_cv_blueprint()
    current_cv = user_interface.get_base_optimized(gen_id)
    messages = user_interface.get_chain_messages(chat_id, closed=True)

    final_call = f"""
        You've interviewd a user about his cv in means to complete the information missing or corrupted in the user data.

        iterview:
        {json.dumps(messages,indent=4)}

        user existing CV:
        {json.dumps(current_cv,indent=4)}

        emend the user data according to the information in the interview:
        1. include all the information from the user data.
        2. emend the infromation according to the information provided in the interview.
        3. try to include has much infromation that is valueable.


        expected format:
        ```json
        {json.dumps(cv_blueprint,indent=4)}
        ```
        """
    cv_data = get_compliation("", final_call, is_json_expected=True)
    user_interface.set_completed_cv_data(cv_data)


def chat_with_agent_to_fill_gaps(user_interface: UserInterface, id, gen_id):
    current_cv = user_interface.get_base_optimized(gen_id)
    issues_to_solve = user_interface.get_issues_to_solve_in_chat(gen_id)

    system_prompt = f"""
    You are an independent HR recruiter, committed to referring the perfect candidate for the job. 
    You help candidates to optimize the CV for the position, optimize the CV.
    you've already optimized the your CV to:
    {json.dumps(current_cv,indent=4)} 

    and have some question to adress:
    {json.dumps(issues_to_solve,indent=4)}

    """
    experience_chatbot(
        system_prompt,
        user_interface,
        id,
        topic="overcoming the gaps between the cv and the position",
    )


def chat_loop(user_interface: UserInterface,position_name:str = None):

    # define the gaps between the position and the CV
    if not user_interface.has_identified_gap_from_hiring_team():
        with user_interface.processing("Finding gaps..."):
            review_by_hiring_team(user_interface,position_name=position_name)
    #
    # optimize what you can optimize and find what not
    gen_id = "first_call"
    if not user_interface.has_optimized_cv(gen_id):
        with user_interface.processing("optimizing..."):
            optimize_and_wonder(user_interface, gen_id)
    #
    # drill with the agent
    chat_id = "overcome_gaps_cv"
    if not user_interface.has_chain_messages(chat_id, closed=True):
        chat_with_agent_to_fill_gaps(user_interface, chat_id, gen_id)

    if not user_interface.has_completed_cv_data() and user_interface.has_chain_messages(
        chat_id, closed=True
    ):
        # update the global CV object
        with user_interface.processing("Applying what i've learned"):
            enrich_from_chat(user_interface, chat_id=chat_id, gen_id=gen_id)
    
        with user_interface.processing("Creating CV options"):
            create_n_optimzied_variation(user_interface, n=1, position_name=position_name)


def multi_agents(user_interface):
    logging_session_id = autogen.runtime_logging.start(config={"dbname": "logs.db"})

    position_data = user_interface.get_position_data()
    cv_data = user_interface.get_completed_cv_data()
    cv_blueprint = user_interface.get_cv_blueprint()
    llm_config = {
        "config_list": [
            {
                "model": "gpt-3.5-turbo",
                "api_key": os.environ["OPENAI_API_KEY"],
                "cache_seed": 42,
            }
        ]
    }
    user_proxy = autogen.UserProxyAgent(
        name="User_proxy",
        description="The User that would like to submit it's CV",
        system_message=f"""You are looking to get an interview, your CV is:
        {json.dumps(cv_data,indent=4)}
        """,
        human_input_mode="ALWAYS",
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
        llm_config=llm_config,
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
        llm_config=llm_config,
    )
    os.environ["WAY"] = "Hiring_technical_recruiter"

    def allowlist(last_speaker: autogen.Agent, groupchat: autogen.GroupChat):
        if last_speaker.name == "User_proxy":
            return list(
                filter(lambda x: x.name == "External_recruiter", groupchat.agents)
            )[0]
        elif last_speaker.name == "Hiring_technical_recruiter":
            return list(
                filter(lambda x: x.name == "External_recruiter", groupchat.agents)
            )[0]
        elif last_speaker.name == "External_recruiter":
            agent = list(
                filter(lambda x: x.name == os.environ["WAY"], groupchat.agents)
            )[0]
            os.environ["WAY"] = (
                "User_proxy"
                if os.environ["WAY"] == "Hiring_technical_recruiter"
                else "External_recruiter"
            )
            return agent
        else:
            raise ValueError()

    recriter_groupchat = autogen.GroupChat(
        agents=[user_proxy, recriter, technical_recriter],
        messages=[],
        max_round=12,
        speaker_selection_method=allowlist,
    )
    manager = autogen.GroupChatManager(
        groupchat=recriter_groupchat, llm_config=llm_config
    )

    result = user_proxy.initiate_chat(
        manager,
        message=f"""Hey there,
    I've come across this amazing job opportunity that I'm really excited about, and I want to make sure my CV is perfectly tailored to it. I've attached the job description below so you can get a sense of what they're looking for.

    Could you please review my CV and make any necessary adjustments to better align it with the job description? I want to make sure I highlight the relevant skills and experiences without making it obvious that I've optimized it. 
    Also, please make sure not to add any information that isn't already in my CV.

    Thanks so much for your help, I really appreciate it!
    My CV:
    {json.dumps(cv_data,indent=4)}
                            
    Position Description:
    {json.dumps(position_data,indent=4)}

        
    """,
    )

    autogen.runtime_logging.stop()

    return result

if __name__ == "__main__":

    terminal_interface = TerminalInterface()
    chat_loop(terminal_interface)
