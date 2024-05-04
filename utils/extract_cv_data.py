import json
from filestore import get_data_from_pdf,get_cv_blueprint,set_user_extract_cv_data,has_user_extract_cv_data,get_user_extract_cv_data
from llm_store import get_compliation
from interface import UserInterface,Args



def core_run(user_interface,pdf_path):
    extracted_text = get_data_from_pdf(pdf_path)
    expected_json = get_cv_blueprint()

    # procrssing
    user_interface.send_user_message("We see the file, We are on it!")
    response =  get_compliation(
        system_message=f"""
                Extract the CV into the following format:
                {json.dumps(expected_json,indent=4)}

                notice: 
                - The input made contains redundant charcthers they to infer which to remove.
                - unicodes are not acceptable outputs.
                - Be sure in every value you include.
                """,
        model="gpt-3.5-turbo-1106",
        temperature=0.1,
        top_p=0,
        user_input=extracted_text,
        is_json_expected=True,
        num_of_gen=2
    )
    return get_compliation(
        system_message="",
        user_input=f"""
                consolidated into one:

                generation #1:  
                {json.dumps(response[0],indent=4)}

                generation #2:  
                {json.dumps(response[1],indent=4)}

                Expected format:
                ```json
                {json.dumps(expected_json,indent=4)}
                ```

                - don't include placeholders!
                """,
        model="gpt-3.5-turbo-1106",
        temperature=0,
        top_p=0,
        is_json_expected=True
    )

def run(user_interface:UserInterface):

    # if the user already have extracted cv data
    if not has_user_extract_cv_data():
        user_extracted_data = None
        for _ in range(3):
            try:
                # get user input
                user_interface.send_user_message("Please upload and PDF file :)")
                pdf_path = user_interface.get_pdf_file_from_user()
                # core logic
                user_extracted_data = core_run(user_interface,pdf_path)
                # saving
                set_user_extract_cv_data(user_extracted_data)
                break
            except Exception as e:
                user_interface.send_user_message("Please add valid path")

        if user_extracted_data:
            user_interface.send_user_message("We got it!")
        else:
            raise ValueError("Try again")
    

if __name__ == "__main__":

        
    collection = list()
    for _ in range(3):
        
        response = core_run(Args(), "data_set/Curriculum_Vitae_Jan24.pdf")

        collection.append(response)

    assert len(set(collection)) == 1
