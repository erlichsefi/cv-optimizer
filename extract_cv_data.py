from PyPDF2 import PdfReader
import json
import os


def extract_text_from_pdf(file):
    text = ""
    with open(file, "rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text


def get_compliation(system_message, user_input, api_key):
    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input},
        ],
        stream=False,
    )
    return stream


def get_expected_cv_data(user_json_filename):
    with open(user_json_filename, "r") as file:
        return json.load(file)


def set_user_cv_data(user_json_filename, user_cv_user):
    with open(user_json_filename, "w") as file:
        return json.dump(user_cv_user, file)


if __name__ == "__main__":
    extracted_text = extract_text_from_pdf("Netanel Erlich- CV.pdf")
    expected_json = get_expected_cv_data("cv.json")
    json_format = get_compliation(
        system_message=f"""
                Extract the CV into the following format:
                {json.dumps(expected_json,indent=4)}
                """,
        user_input=extracted_text,
        api_key=os.environ["OPENAI_API_KEY"],
    )

    user_extracted_data = json.loads(json_format.choices[0].message.content)
    set_user_cv_data(
        user_json_filename="user_cv.json", user_cv_user=user_extracted_data
    )
