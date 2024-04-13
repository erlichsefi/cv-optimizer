import streamlit as st
import asyncio
from autogen import AssistantAgent, UserProxyAgent
import os


st.set_page_config(page_title="Proxy agent")



st.write("""# Using AutoGen Chat Agents""")

class TrackableAssistantAgent(AssistantAgent):
    def _process_received_message(self, message, sender, silent):
        with st.chat_message(sender.name):
            st.markdown(message)
        return super()._process_received_message(message, sender, silent)


class TrackableUserProxyAgent(UserProxyAgent):
    def _process_received_message(self, message, sender, silent):
        with st.chat_message(sender.name):
            st.markdown(message)
        return super()._process_received_message(message, sender, silent)



def extract_text_from_pdf(file):
    from tempfile import NamedTemporaryFile
    from PyPDF2 import PdfReader

    with NamedTemporaryFile(dir='.', suffix='.pdf') as f:
        f.write(file.getbuffer())

        text = ""
        with open(f.name, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
        return text
    

prompt_value = """Hey there,

I've come across this amazing job opportunity that I'm really excited about, and I want to make sure my CV is perfectly tailored to it. I've attached the job description below so you can get a sense of what they're looking for.

Could you please review my CV and make any necessary adjustments to better align it with the job description? I want to make sure I highlight the relevant skills and experiences without making it obvious that I've optimized it. Also, please make sure not to add any information that isn't already in my CV.

Thanks so much for your help, I really appreciate it!
My CV:
{cv_text}
                        
Position Description:
{position}

      
"""
prompt = st.text_area("The prompt",value=prompt_value, height=int(len(prompt_value)/2))



with st.container():
    if st.button("Let's go."):
        
        if 'uploaded_file' not in st.session_state or st.session_state['uploaded_file'] is None:
            st.warning("Please upload file")
            st.stop()

        cv_text = extract_text_from_pdf(st.session_state['uploaded_file'])


        if "position" not in st.session_state or st.session_state['position'] is None and len(st.session_state['position']) > 10:
            st.warning("Please fill position details")
            st.stop()

        api_key = os.environ.get("OPENAI_API_KEY",None)
        if "oai_key" not in st.session_state or st.session_state['oai_key'] is None  or not st.session_state['oai_key'].startswith("sk"):
            st.toast("here you go, a free api call to openai")
        else:
            api_key = st.session_state['oai_key']
            st.toast("ok ok... using your token")

        llm_config = {
            # "request_timeout": 600,
            "config_list": [
                {
                    "model": "gpt-3.5-turbo",
                    "api_key": api_key
                }
            ]
        }
        # create an AssistantAgent instance named "assistant"
        assistant = TrackableAssistantAgent(
            name="assistant", llm_config=llm_config)

        # create a UserProxyAgent instance named "user"
        user_proxy = TrackableUserProxyAgent(
            name="user", human_input_mode="NEVER", llm_config=llm_config, code_execution_config=False)

        # Create an event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Define an asynchronous function
        async def initiate_chat():
            await user_proxy.a_initiate_chat(
                assistant,
                message=prompt.format(cv_text=cv_text,position=st.session_state['position']),
            )

        # Run the asynchronous function within the event loop
        loop.run_until_complete(initiate_chat())