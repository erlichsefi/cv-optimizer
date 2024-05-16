import utils


def execute(user_interface:utils.UserInterface):

    # if the user already have extracted cv data
    if not user_interface.has_user_extract_cv_data():
        user_extracted_data = None
        for _ in range(3):
            try:
                # get user input
                user_interface.send_user_message("Please upload and PDF file :)")
                pdf_path = user_interface.get_pdf_file_from_user()
                # core logic
                user_extracted_data = utils.pdf_to_user_data(user_interface,pdf_path)
                # saving
                user_interface.set_user_extract_cv_data(user_extracted_data)
                break
            except Exception as e:
                user_interface.send_user_message("Please add valid path")

        if user_extracted_data:
            user_interface.send_user_message("We got it!")
        else:
            raise ValueError("Try again")


    # ask the user about the data
    if not user_interface.has_completed_cv_data():
        
        utils.verify_user_data(user_interface)

        user_interface.send_user_message("We got it! Thanks!")
        user_interface.send_user_message("Moving on...")

    # ask the user to upload position snippet
    if not user_interface.has_position_data():
        user_interface.send_user_message("Moving on...")
        user_interface.send_user_message("Yalla, paste the position you would like to get interview for:")
        contents = user_interface.get_position_snippet_data()
        utils.position_snippet_to_position_data(user_interface,contents)

        user_interface.send_user_message("Done! :)")

    # overcome gaps
    if not user_interface.has_position_cv_offers():
        utils.overcome_gaps(user_interface)

    # to pdfs
    utils.to_pdfs(user_interface)