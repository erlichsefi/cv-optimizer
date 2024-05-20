import json
from .llm_store import get_compliation
from .interface import UserInterface, Args


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
    user_interface.on_cv_file_received()
    response = get_compliation(
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
        num_of_gen=2,
    )

    user_extracted_data =  get_compliation(
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
        is_json_expected=True,
    )
    user_interface.set_user_extract_cv_data(user_extracted_data,pdf_path)


if __name__ == "__main__":

    collection = list()
    for _ in range(3):

        response = core_run(Args(), "data_set/Curriculum_Vitae_Jan24.pdf")

        collection.append(response)

    diff = dict_diff(collection[2], collection[1])
    for entry in diff:
        for index in range(len(collection[2][entry])):
            print(dict_diff(collection[2][entry][index], collection[1][entry][index]))

    assert len(set(collection)) == 1
