import json
from .filestore import get_data_from_pdf,get_cv_blueprint,set_user_extract_cv_data,has_user_extract_cv_data
from .llm_store import get_compliation
from .interface import UserInterface



def run(user_interface:UserInterface):

    # if the user already have extracted cv data
    if not has_user_extract_cv_data():
        user_extracted_data = None
        for _ in range(3):
            try:
                # get user input
                user_interface.send_user_message("Please upload and PDF file :)")
                pdf_path = user_interface.get_pdf_file_from_user()
                extracted_text = get_data_from_pdf(pdf_path)
                expected_json = get_cv_blueprint()

                # procrssing
                user_interface.send_user_message("We see the file, We are on it!")
                user_extracted_data = get_compliation(
                    system_message=f"""
                            Extract the CV into the following format:
                            {json.dumps(expected_json,indent=4)}
                            """,
                    user_input=extracted_text,
                    is_json_expected=True
                )

                # saving
                set_user_extract_cv_data(user_extracted_data)
                break
            except Exception:
                user_interface.send_user_message("Please add valid path")

        if user_extracted_data:
            user_interface.send_user_message("We got it!")
        else:
            raise ValueError("Try again")
    

if __name__ == "__main__":
    run(pdf_path="Curriculum_Vitae_Jan24.pdf")
