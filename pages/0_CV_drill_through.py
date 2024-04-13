from openai import OpenAI
import streamlit as st

st.title("CV Drill Through")
st.markdown("""
            Are you sure you've included everything that can help you get this position?\n
            Let's an agnet interview you to find more details you've missed!\n
            Future work will drill through your Github and Linkedin profiles.\n
            """)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
system_message = """
I need you to drill through my CV and the position details i will provide you.

Position details:
{position}

CV:
{cv_text}

provide a short and consice question in a mean my to find information that i've missed from my CV and can enrich my CV.
"""

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


def get_compliation(position,cv_text):
    stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=
            [
             {"role":"system","content":system_message.format(cv_text=cv_text,position=position)}
            ]+
            [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
    return st.write_stream(stream)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    print(message)
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state['messages'] or st.button("Drill Down with me"):
    # check the file was up
    if (
        "uploaded_file" not in st.session_state
        or st.session_state["uploaded_file"] is None
    ):
        st.warning("Please upload file")
        st.stop()

    # check the position details 
    if (
        "position" not in st.session_state
        or st.session_state["position"] is None
        or len(st.session_state["position"]) < 10
    ):
        st.warning("Please fill position details")
        st.stop()

    # extract details
    cv_text = extract_text_from_pdf(st.session_state["uploaded_file"])
    position = st.session_state["position"]
    
    # agent ask the first question
    with st.chat_message("assistant"):
        response = get_compliation(position,cv_text)
        # st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

    if prompt := st.chat_input("What is up?"):
        
        # add the message to messages
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})