
import json
import os
from filestore import get_position_blueprint,set_position_data
from llm_store import get_compliation



if __name__ == "__main__":
    expected_json = get_position_blueprint()
    user_input = input("Paste the position infromation")
    json_format = get_compliation(
        system_message=f"""
                Extract the Position into the following format:
                {json.dumps(expected_json,indent=4)}
                """,
        user_input=user_input
    )

    user_extracted_data = json.loads(json_format.choices[0].message.content)
    set_position_data(user_extracted_data)
