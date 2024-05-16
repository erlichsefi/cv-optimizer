import streamlit as st
import openai
import utils


streamlit = utils.SteamlitInterface()
# Initialize session state to store chat history and conversations
if 'conversations' not in st.session_state:
    st.session_state.conversations = {}
    st.session_state.current_conversation = 'Conversation 1'
    st.session_state.show_upload_popup = False  # To manage the popup display

# Function to generate a response from OpenAI
def get_response(user_input):
    response = openai.Completion.create(
        engine="text-davinci-003",  # Use appropriate model
        prompt=user_input,
        max_tokens=150
    )
    return response.choices[0].text.strip()


@st.experimental_dialog("Setup your CV")
def upload_cv():
    # 
    utils.pdf_to_user_data(streamlit)

    # ask the user about the data
    utils.verify_user_data(streamlit)

# Button to show the upload popup
if st.sidebar.button("Upload CV"):
    upload_cv()

# Manage the popup display
if st.session_state.show_upload_popup:
    upload_cv()

st.sidebar.title("Positions")
conversation_names = list(st.session_state.conversations.keys())

if st.sidebar.button("New Position"):
    new_conversation_name = f"Conversation {len(conversation_names) + 1}"
    st.session_state.conversations[new_conversation_name] = []
    st.session_state.current_conversation = new_conversation_name
    st.experimental_rerun()

if conversation_names:
    st.session_state.current_conversation = st.sidebar.radio(
        "Select position", conversation_names, index=conversation_names.index(st.session_state.current_conversation))

# Display current conversation history
current_conversation = st.session_state.current_conversation
st.title(f"ChatGPT-like Interface - {current_conversation}")

if current_conversation not in st.session_state.conversations:
    st.session_state.conversations[current_conversation] = []

for i, msg in enumerate(st.session_state.conversations[current_conversation]):
    if i % 2 == 0:
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**ChatGPT:** {msg}")

# User input
user_input = st.text_input("You:")

# When the user submits input
if st.button("Send"):
    if user_input:
        # Append user message to chat history
        st.session_state.conversations[current_conversation].append(user_input)

        # Generate response
        response = get_response(user_input)

        # Append ChatGPT's response to chat history
        st.session_state.conversations[current_conversation].append(response)

        # Clear the input box
        st.experimental_rerun()
