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
            "Upload your current CV: (required)", type="pdf"
        )

    # Add position information
    value = ""
    if "position" in st.session_state and st.session_state["position"] is not None:
        value = st.session_state["position"]
    st.session_state["position"] = st.text_area(
        "The poistion copied details: (required)", value=value
    )

    # add you open-ai key
    st.header("OpenAI Configuration:")
    value = None
    if "oai_key" in st.session_state and st.session_state["oai_key"] is not None:
        value = st.session_state["oai_key"]

    st.session_state["oai_key"] = st.text_input("API Key (optional)", type="password",value=value)
    st.text("Notice:\n keeping the API key field empty\n will cause using my own private\n API key and hence will presistence\n the cv and position details. ")


st.markdown(
    """
 This tool is designed to assist you in tailoring your CV to a specific position you're interested in pursuing.

## How to Begin?
- Begin by uploading your PDF CV in the sidebar.
- Paste the job details into the sidebar. (Include only the information you want to optimize your CV based on)
- Choose a method (from the sidebar) and navigate to its respective page.

## Methods available:
1. Is there any infromation you've missed from you CV that can help you get the position? an LLN agent will drtill through your CV and position to help you find details to add to the CV.
2. Providing your CV and position details in a single prompt to the LLM, guiding it to align the CV to the position.
   - You can adjust the prompt on the method page.
3. Requesting an LLM agent the represnet you in the CV improvemtns.
   - You can refine your intent on the method page.

### Important Note:
   - This tool utilizes generative AI in a basic manner, and there are no guarantees for the output accuracy.
   - This tool is free to use by providing your own OpenAI key, however if you keep the API key field empty i will store your input and the prompt used for exploration purpose.

## Looking for a job?
I'm continuously exploring new methods to improve this tool. Would like to prove your skills? contribute to the code.
Additioanly, If you have any suggestions or ideas, please feel free to reach out to me at erlichsefi@gmail.com.

"""
)
