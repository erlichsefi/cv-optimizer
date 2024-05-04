import utils


def execute(user_interface):
    utils.pdf_to_user_data(user_interface)

    # ask the user about the data
    utils.verify_user_data(user_interface)

    # ask the user to upload position snippet
    utils.position_snippet_to_position_data(user_interface)

    # overcome gaps
    utils.overcome_gaps(user_interface)

    # to pdfs
    utils.to_pdfs(user_interface)