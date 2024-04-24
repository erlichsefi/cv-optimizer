from utils.extract_cv_data import run
from utils.complete_missing_data import get_questions,set_value_at_xpath
import streamlit as st
import os

st.title("Let's start by uploading your CV:")
        


def extract_text_from_pdf(file):
    from tempfile import NamedTemporaryFile
    from PyPDF2 import PdfReader

    with NamedTemporaryFile(dir=".", suffix=".pdf") as f:
        f.write(file.getbuffer())

        text = ""
        with open(f.name, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
        return text


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

if st.button("Yalla!") or "user_data" in st.session_state:   

    if "user_data" not in st.session_state:   
        st.session_state["user_data"] = run(cv_path=st.session_state["uploaded_file"],cv_json_format_path="cv.json",output_path="user_data/user.json")
    
    st.write("We is the data we found:")
    st.write(st.session_state["user_data"])

    if st.button("Couple of follow ups!") or "questions" in st.session_state:

        if 'questions' not in st.session_state:
            st.session_state['questions'] = get_questions("user_data/user.json")

        st.write("We is the questions we have:")
        st.write(st.session_state["questions"])

        st.session_state["user_data_v2"] = st.session_state["user_data"].copy()

                    

        input_values = []
        for index,question in enumerate(st.session_state['questions']):
            input_value = st.text_input(label=question['question'])
            input_values.append(input_value)

        if st.button("Done"):
            for value,question in zip(input_values,st.session_state['questions']):
                print(value)
                set_value_at_xpath(st.session_state["user_data_v2"],question['target_missing'],value)
            st.write(st.session_state["user_data_v2"])
            

