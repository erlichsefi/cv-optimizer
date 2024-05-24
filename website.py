import streamlit as st
import utils
import time



# Initialize session state to store chat history and conversations
if "conversations" not in st.session_state:
    st.session_state.application_session = utils.SteamlitInterface()
    st.session_state.conversations = {}

    if st.session_state.application_session.has_position_data():
        mem_positions = st.session_state.application_session.get_position_data()
        if mem_positions:
            st.session_state.conversations = dict([ (k,[])for k in mem_positions.keys()])
            st.session_state.current_conversation = list(mem_positions.keys())[0]

    st.session_state.show_upload_popup = False  # To manage the popup display
    st.session_state.show_position_upload_popup = False
    

    
conversation_names = list(st.session_state.conversations.keys())

@st.experimental_dialog("Setup your CV")
def upload_cv():
    #
    pdf_path = st.session_state.application_session.get_pdf_file_from_user()
    if pdf_path is not None:
        with st.session_state.application_session.processing("Processing the file..."):
            utils.pdf_to_user_data(st.session_state.application_session, pdf_path)
        # Process the uploaded file if needed
        st.session_state.show_upload_popup = False  # Close the popup after uploading
        st.success("CV uploaded successfully!")
        st.rerun()


st.sidebar.title("Profile")

if not st.session_state.application_session.has_user_extract_cv_data():
    if st.sidebar.button("Upload CV"):
        upload_cv()
else:
    filename = st.session_state.application_session.get_user_extract_cv_file_name()
    if st.sidebar.button(f"Remove '{filename}'"):
        st.session_state.application_session.unset_user_extract_cv_data()
        st.rerun()

    if not st.session_state.application_session.has_completed_cv_data():
        utils.verify_user_data(st.session_state.application_session)
    else:
        if not conversation_names:
            st.write("Please upload a position data before continue")
                



st.sidebar.title("Positions")


@st.experimental_dialog("New position")
def upload_new_position():
    #
    contents = st.session_state.application_session.get_position_snippet_data()
    if contents is not None:
        with st.session_state.application_session.processing("Processing Position..."):
            new_conversation_name = utils.position_snippet_to_position_data(
                st.session_state.application_session, contents
            )

        st.session_state.show_position_upload_popup = False
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

    if not st.session_state.application_session.has_position_cv_offers(current_conversation):
        utils.overcome_gaps(st.session_state.application_session,position_name=current_conversation)
    
    if st.session_state.application_session.has_position_cv_offers(current_conversation) and not st.session_state.application_session.has_pdfs_files(current_conversation):
        with st.session_state.application_session.processing("Exporting..."):
            utils.to_pdfs(st.session_state.application_session,current_conversation=current_conversation)
    else:
        print()

    if current_conversation not in st.session_state.conversations:
        st.session_state.conversations[current_conversation] = []
        #