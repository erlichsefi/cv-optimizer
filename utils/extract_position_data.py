
import json
from filestore import get_position_blueprint,set_position_data
from llm_store import get_compliation



if __name__ == "__main__":
    expected_json = get_position_blueprint()
    user_input = input("Paste the position infromation")
    user_extracted_data = get_compliation(
        system_message=f"""
                Extract the Position into the following format:
                {json.dumps(expected_json,indent=4)}
                """,
        user_input=user_input,
        is_json_expected=True
    )

    set_position_data(user_extracted_data)
