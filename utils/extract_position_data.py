import json
from .llm_store import get_compliation
from .interface import TerminalInterface, UserInterface


def run(user_interface: UserInterface, contents: str):
    expected_json = user_interface.get_position_blueprint()
    user_extracted_data = get_compliation(
        system_message=f"""
                Extract the Position into the following format:
                {json.dumps(expected_json,indent=4)}
                """,
        user_input=contents,
        is_json_expected=True,
    )

    position_name = (
        f"{user_extracted_data['job_title']} @ {user_extracted_data['company']}"
    )
    user_interface.set_position_data(position_name, user_extracted_data)

    return position_name


if __name__ == "__main__":
    terminal = TerminalInterface()
    run(terminal)
