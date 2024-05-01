
from utils import TerminalInterface,pdf_to_user_data,verify_user_data,position_snippet_to_position_data,overcome_gaps,to_pdfs



if __name__ == "__main__":
    termianl = TerminalInterface()

    termianl.send_user_message("Please upload and PDF file :)")
    
    pdf_path = termianl.get_user_input()

    #TODO: validate the path
    pdf_to_user_data(pdf_path)

    # ask the user about the data
    verify_user_data(termianl)

    # ask the user to upload position snippet
    position_snippet_to_position_data(termianl)

    # overcome gaps
    overcome_gaps(termianl)

    # to pdfs
    pdf_paths = to_pdfs()

    termianl.send_user_message(pdf_paths)











