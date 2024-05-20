import streamlit as st
import utils


# Initialize session state to store chat history and conversations
if "conversations" not in st.session_state:
    st.session_state.conversations = {}
    # st.session_state.current_conversation = 'Conversation 1'
    st.session_state.show_upload_popup = False  # To manage the popup display
    st.session_state.show_position_upload_popup = False
    st.session_state.application_session = utils.SteamlitInterface()


@st.experimental_dialog("Setup your CV")
def upload_cv():
    #
    pdf_path = st.session_state.application_session.get_pdf_file_from_user()
    if pdf_path is not None:
        with st.spinner("Processing the file..."):
            utils.pdf_to_user_data(st.session_state.application_session, pdf_path)
        # Process the uploaded file if needed
        st.session_state.show_upload_popup = False  # Close the popup after uploading
        st.success("CV uploaded successfully!")
        #
        #
        # st.write("Couple of question:")
        # utils.verify_user_data(st.session_state.application_session)

        st.rerun()


st.sidebar.title("Profile")
# Button to show the upload popup

if not st.session_state.application_session.has_user_extract_cv_data():
    if st.sidebar.button("Upload CV"):
        upload_cv()
else:
    filename = st.session_state.application_session.get_user_extract_cv_file_name()
    if st.sidebar.button(f"Remove '{filename}'"):
        st.session_state.application_session.unset_user_extract_cv_data()


st.sidebar.title("Positions")
conversation_names = list(st.session_state.conversations.keys())


@st.experimental_dialog("New position")
def upload_new_position():
    #
    contents = st.session_state.application_session.get_position_snippet_data()
    if contents is not None:
        with st.spinner("Processing Position..."):
            new_conversation_name = utils.position_snippet_to_position_data(
                st.session_state.application_session, contents
            )
        # Process the uploaded file if needed
        st.session_state.show_position_upload_popup = (
            False  # Close the popup after uploading
        )
        st.success("Position uploaded successfully!")

        # set new poisition
        st.session_state.conversations[new_conversation_name] = []
        st.session_state.current_conversation = new_conversation_name
        st.rerun()


if st.sidebar.button("New Position"):
    upload_new_position()


if conversation_names:
    st.session_state.current_conversation = st.sidebar.radio(
        "Select position",
        conversation_names,
        index=conversation_names.index(st.session_state.current_conversation),
    )

# Display current conversation history

if st.session_state.get("current_conversation", None) is None:
    st.write("please select a poisition")
else:
    current_conversation = st.session_state.current_conversation
    st.title(f"{current_conversation}")

    if current_conversation not in st.session_state.conversations:
        st.session_state.conversations[current_conversation] = []

    utils.overcome_gaps(st.session_state.application_session)

    # When the user submits input
    if st.button("Send"):
        pass
        # if user_input:
        #     # Append user message to chat history
        #     st.session_state.conversations[current_conversation].append(user_input)

        #     # Generate response
        #     response = get_response(user_input)

        #     # Append ChatGPT's response to chat history
        #     st.session_state.conversations[current_conversation].append(response)

        #     # Clear the input box
        #     st.experimental_rerun()
