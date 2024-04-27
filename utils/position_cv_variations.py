
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
        description="The User that would like to submit it's CV",
        system_message=f"""You are looking to get an interview, your CV is:
        {json.dumps(cv_data,indent=4)}
        """,
        human_input_mode="ALWAYS"
    )
    recriter = autogen.AssistantAgent(
        name="Technical_recruiter",
        description="an technical recruiter in the hiring compeny",
        system_message=f"""You are an experienced technical recruiter tasked with filling an open position in a leading tech company. 
        Your goal is to find the best candidate who not only possesses the necessary technical skills but 
        also fits well with the company culture. Write a job description for the position of technical recruiter,
          outlining the key responsibilities, required qualifications, and desired attributes. 
        Additionally, draft a message to be posted on relevant job boards and social media platforms to attract potential candidates. 
        Be concise, professional, and engaging in your communication.
        You're only to given feedback!

        The position is:
        {json.dumps(position_data,indent=4)}
        
        """,
        llm_config=llm_config
    )
    technical_recriter = autogen.AssistantAgent(
        name="External_recruiter",
        description="external HR recruite that will help me get the position",
        system_message=f"""
        You are HR external recruiter, committed to refer the perfect candidate for the job. 
        You refer a candidte to the position and see the recruiter reaction and then adjust the candidate CV and try again.
       
        CV must be ion the following format:
        {json.dumps(cv_blueprint,indent=4)}
        """,
        llm_config=llm_config
    )
    os.environ['WAY'] = "Technical_recruiter"
    def allowlist(last_speaker: autogen.Agent, groupchat: autogen.GroupChat):
        if last_speaker.name == "User_proxy":
            return list(filter(lambda x: x.name == "External_recruiter",groupchat.agents))[0]
        elif last_speaker.name == "Technical_recruiter":
            return list(filter(lambda x: x.name == "External_recruiter",groupchat.agents))[0]
        elif last_speaker.name == "External_recruiter":
            agent =  list(filter(lambda x: x.name == os.environ['WAY'],groupchat.agents))[0]
            os.environ['WAY'] = "User_proxy" if os.environ['WAY'] == "Technical_recruiter" else "External_recruiter"
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
    result
if __name__ == "__main__":
    multi_agents()




   











