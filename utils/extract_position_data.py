import json
from .llm_store import get_compliation
from .interface import TerminalInterface, UserInterface


def run(user_interface: UserInterface, contents: str):
    user_interface.send_user_message("We got the position data, working on it...")
    expected_json = user_interface.get_position_blueprint()
    user_extracted_data = get_compliation(
        system_message=f"""
                Extract the Position into the following format:
                {json.dumps(expected_json,indent=4)}
                """,
        user_input=contents,
        is_json_expected=True,
    )

    user_interface.set_position_data(user_extracted_data)

    return f"{user_extracted_data['job_title']} @ {user_extracted_data['company']}"


if __name__ == "__main__":
    terminal = TerminalInterface()
    run(terminal)
