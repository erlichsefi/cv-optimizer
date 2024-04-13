import streamlit as st
import dotenv
import os

dotenv.load_dotenv(".env")  
st.set_page_config(
    page_title="Wellcome",
    page_icon="👋",
)

st.write("# Welcome to CV optimiztion to a certain position! 👋")

with st.sidebar:

    st.header("Your details:")

    # add CV
    value = ""
    if (
        "uploaded_file" in st.session_state
        and st.session_state["uploaded_file"] is not None
    ):

        if st.button(f"Remove '{st.session_state['uploaded_file'].name}'"):
            st.session_state.pop("uploaded_file")
            st.rerun()
    else:
        st.session_state["uploaded_file"] = st.file_uploader(
            "Upload your current CV", type="pdf"
        )

    # Add position information
    value = ""
    if "position" in st.session_state and st.session_state["position"] is not None:
        value = st.session_state["position"]
    st.session_state["position"] = st.text_area(
        "The poistion copied details:", value=value
    )

    # add you open-ai key
    st.header("OpenAI Configuration:")
    st.session_state["oai_key"] = st.text_input("API Key (Optinal)", type="password")
    st.text("Notice:\n keeping the API key field empty\n will cause using my own API key\n and will cause presistence of cv and position details. ")


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
