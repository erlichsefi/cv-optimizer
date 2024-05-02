
import utils


if __name__ == "__main__":
    termianl = utils.TerminalInterface()

    utils.pdf_to_user_data(termianl)

    # ask the user about the data
    utils.verify_user_data(termianl)

    # ask the user to upload position snippet
    utils.position_snippet_to_position_data(termianl)

    # overcome gaps
    utils.overcome_gaps(termianl)

    # to pdfs
    utils.to_pdfs()










