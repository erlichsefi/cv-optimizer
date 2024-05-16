import json
from .llm_store import get_compliation
from .interface import UserInterface,Args

def dict_diff(dict1, dict2):
    diff = {}
    all_keys = set(dict1.keys()) | set(dict2.keys())
    for key in all_keys:
        if key not in dict2:
            diff[key] = (dict1[key], None)
        elif key not in dict1:
            diff[key] = (None, dict2[key])
        elif isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
            nested_diff = dict_diff(dict1[key], dict2[key])
            if nested_diff:
                diff[key] = nested_diff
        elif dict1[key] != dict2[key]:
            diff[key] = (dict1[key], dict2[key])
    return diff

def core_run(user_interface, pdf_path):
    extracted_text = user_interface.get_data_from_pdf(pdf_path)
    expected_json = user_interface.get_cv_blueprint()

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
        temperature=0.2,
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
    if not user_interface.has_user_extract_cv_data():
        user_extracted_data = None
        for _ in range(3):
            try:
                # get user input
                user_interface.send_user_message("Please upload and PDF file :)")
                pdf_path = user_interface.get_pdf_file_from_user()
                # core logic
                user_extracted_data = core_run(user_interface,pdf_path)
                # saving
                user_interface.set_user_extract_cv_data(user_extracted_data)
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
    
    diff = dict_diff(collection[2],collection[1])
    for entry in diff:
        for index in range(len(collection[2][entry])):
            print(dict_diff(collection[2][entry][index],collection[1][entry][index]))

    assert len(set(collection)) == 1
