
import json
from filestore import get_position_blueprint,set_position_data
from llm_store import get_compliation



if __name__ == "__main__":
    expected_json = get_position_blueprint()
    print("Enter/Paste your content. Ctrl-D or Ctrl-Z ( windows ) to save it.")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    user_extracted_data = get_compliation(
        system_message=f"""
                Extract the Position into the following format:
                {json.dumps(expected_json,indent=4)}
                """,
        user_input="\n".join(contents),
        is_json_expected=True
    )

    set_position_data(user_extracted_data)
