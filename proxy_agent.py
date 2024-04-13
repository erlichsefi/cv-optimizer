import streamlit as st
import asyncio
from autogen import AssistantAgent, UserProxyAgent
import os,dotenv
from cv import extract_text_from_pdf
dotenv.load_dotenv(".env")

st.write("""# AutoGen Chat Agents""")

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


selected_model = "gpt-3.5-turbo"
selected_key = os.environ['OPENAI_API_KEY']

uploaded_file = st.file_uploader("Upload your current CV", type="pdf")

position = st.text_area("The poistion copied details:")

#st.text_area("The prompt",value=
prompt = """Hey there,

I hope you're doing well! I need your help with something important. I've come across this amazing job opportunity that I'm really excited about, and I want to make sure my CV is perfectly tailored to it. I've attached the job description below so you can get a sense of what they're looking for.

Could you please review my CV and make any necessary adjustments to better align it with the job description? I want to make sure I highlight the relevant skills and experiences without making it obvious that I've optimized it. Also, please make sure not to add any information that isn't already in my CV.

Thanks so much for your help, I really appreciate it!
My CV:
{cv_text}
                        
Position Description:
{position}
                        
"""


with st.container():
    # for message in st.session_state["messages"]:
    #    st.markdown(message)

    if st.button("Let's go."):
        cv_text = extract_text_from_pdf(uploaded_file)
        if not selected_key or not selected_model:
            st.warning(
                'You must provide valid OpenAI API key and choose preferred model', icon="⚠️")
            st.stop()

        llm_config = {
            # "request_timeout": 600,
            "config_list": [
                {
                    "model": selected_model,
                    "api_key": selected_key
                }
            ]
        }
        code_execution_config = {"work_dir": "web", "use_docker": False}
        # create an AssistantAgent instance named "assistant"
        assistant = TrackableAssistantAgent(
            name="assistant", llm_config=llm_config)

        # create a UserProxyAgent instance named "user"
        user_proxy = TrackableUserProxyAgent(
            name="user", human_input_mode="NEVER", llm_config=llm_config, code_execution_config=code_execution_config)

        # Create an event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Define an asynchronous function
        async def initiate_chat():
            await user_proxy.a_initiate_chat(
                assistant,
                message=prompt.format(cv_text=cv_text,position=position),
            )

        # Run the asynchronous function within the event loop
        loop.run_until_complete(initiate_chat())