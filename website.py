import streamlit as st
import utils
from streamlit_pdf_viewer import pdf_viewer


st.sidebar.image("title.png")

# Initialize session state to store chat history and conversations
if "conversations" not in st.session_state:
    st.session_state.application_session = utils.SteamlitInterface()
    st.session_state.conversations = {}

    if st.session_state.application_session.has_position_data():
        mem_positions = st.session_state.application_session.get_position_data()
        if mem_positions:
            st.session_state.conversations = dict([ (k,[])for k in mem_positions.keys()])
            st.session_state.current_conversation = list(mem_positions.keys())[0]

    st.session_state.show_pdf_upload_popup = False  # To manage the popup display
    st.session_state.show_position_upload_popup = False

    
if not st.session_state.application_session.get_user_extract_cv_data():
    st.markdown("# Hi, there! :wave: ")
    st.markdown(" ### We are here to help YOU get the interview for your next position!")
    st.write("We're here to help you create the best CV the quickly as possible")
    st.write("To start, upload your CV by clicking the 'Upload CV' on the left")
    st.write(":point_left: :point_left:")

    
conversation_names = list(st.session_state.conversations.keys())

@st.experimental_dialog("Setup your CV")
def upload_cv():
    #
    pdf_path = st.session_state.application_session.get_pdf_file_from_user()
    if pdf_path is not None:
        with st.session_state.application_session.processing("Processing the file..."):
            utils.pdf_to_user_data(st.session_state.application_session, pdf_path)
        # Process the uploaded file if needed
        st.session_state.show_pdf_upload_popup = False  # Close the popup after uploading
        st.success("CV uploaded successfully!")
        st.rerun()


st.sidebar.title("Profile")

if not st.session_state.application_session.has_user_extract_cv_data():
    if st.sidebar.button("Upload CV") or st.session_state.show_pdf_upload_popup:
        st.session_state.show_pdf_upload_popup = True
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
            st.markdown("# Now, we know you!")
            st.markdown("From here on, you only need to provide the position you are instrestd in")
            st.write("You just need to add the position data, upload your CV by clicking the New Position' on the left")
            st.write(":point_left: :point_left:")
                


# Quit twice.
# Loader when chat it created


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

if st.sidebar.button("New Position") or st.session_state.show_position_upload_popup:
    st.session_state.show_position_upload_popup = True
    upload_new_position()

if conversation_names:
    st.session_state.current_conversation = st.sidebar.radio(
        "Select position",
        conversation_names,
        index=conversation_names.index(st.session_state.current_conversation),
    )

# Display current conversation history
if not st.session_state.get("current_conversation", None) is None:
    current_conversation = st.session_state.current_conversation
    st.title(f"{current_conversation}")

    if not st.session_state.application_session.has_position_cv_offers(current_conversation):
        utils.overcome_gaps(st.session_state.application_session,position_name=current_conversation)
    
    if st.session_state.application_session.has_position_cv_offers(current_conversation) and not st.session_state.application_session.has_pdfs_files(current_conversation):
        with st.session_state.application_session.processing("Exporting..."):
            utils.to_pdfs(st.session_state.application_session,current_conversation=current_conversation)
            st.rerun()
            
    if st.session_state.application_session.has_pdfs_files(current_conversation):
        cv_offers = st.session_state.application_session.get_pdfs_files(current_conversation)
        overletters = st.session_state.application_session.get_all_position_cv_cover_letters(current_conversation)

        

        st.markdown("### Message to hiring team:")
        st.write(overletters[0])
        st.markdown("### CV to apply with:")
        pdf_viewer(cv_offers[0])

        with open(cv_offers[0], "rb") as pdf_file:
            PDFbyte = pdf_file.read()

        st.download_button("Pay and Download",PDFbyte,file_name="cv.pdf",
                    mime='application/octet-stream')

    if current_conversation not in st.session_state.conversations:
        st.session_state.conversations[current_conversation] = []
        #