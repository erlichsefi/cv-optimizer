import streamlit as st
import dotenv

dotenv.load_dotenv(".env") # load .env
st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to CV optimiztion to a certain position! 👋")

# selected_model = None
# selected_key = None
with st.sidebar:
    # st.header("OpenAI Configuration")
    # selected_model = st.selectbox("Model", ['gpt-3.5-turbo', 'gpt-4'], index=1)
    # selected_key = st.text_input("API Key", type="password")

    st.header("Your details:")
    value = ""
    if "uploaded_file" in st.session_state and st.session_state['uploaded_file'] is not None:
        
        if st.button(f"Remove '{st.session_state['uploaded_file'].name}'"):
            st.session_state.pop("uploaded_file")
            st.rerun()
    else:
        st.session_state['uploaded_file'] = st.file_uploader("Upload your current CV", type="pdf")

    value = ""
    if "position" in st.session_state and st.session_state['position'] is not None:
        value = st.session_state['position']
    st.session_state['position'] = st.text_area("The poistion copied details:",value=value)

st.markdown(
    """
    This application is intented to help you customize your CV to a position you would like to get. 


    # How to start?
       - Upload Your pdf CV into the sidebar.
       - Copy the position details into the sidebar. (include only information you would like to optimize your CV base on)
       - Select a method (from the sidebar) and move to it's page.

    # Currently, there are two methods:
       1. Simple providing the CV and position when calling the LLM with a single prompt.
           - you can adjust the prompt in the method page.
       2. Asking an LLM agent to represent the user.
           - you can adjust your intent in the method page.


    ## Important!
    This is a simple use of genrative AI and there is no guarantee for any of the produce. 

    I'm still exploring methods to do so, so if you have any idea, please let me know at erlichsefi@gmail.com


"""
)