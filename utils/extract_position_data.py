
import json
from filestore import get_position_blueprint,set_position_data
from llm_store import get_compliation
from interface import TerminalInterface


if __name__ == "__main__":
    expected_json = get_position_blueprint()
    contents = TerminalInterface().get_multiliner_user_input()
    user_extracted_data = get_compliation(
        system_message=f"""
                Extract the Position into the following format:
                {json.dumps(expected_json,indent=4)}
                """,
        user_input=contents,
        is_json_expected=True
    )

    set_position_data(user_extracted_data)
