import json
import os
from filestore import get_data_from_pdf,get_cv_blueprint,set_user_extract_cv_data
from llm_store import get_compliation



def run(pdf_path):
    extracted_text = get_data_from_pdf(pdf_path)
    expected_json = get_cv_blueprint()
    user_extracted_data = get_compliation(
        system_message=f"""
                Extract the CV into the following format:
                {json.dumps(expected_json,indent=4)}
                """,
        user_input=extracted_text,
        is_json_expected=True
    )
    set_user_extract_cv_data(user_extracted_data)


if __name__ == "__main__":
    run(pdf_path="Curriculum_Vitae_Jan24.pdf")
