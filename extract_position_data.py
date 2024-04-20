from PyPDF2 import PdfReader
import json
import os


user_input = """
Job Title: Senior Data Scientist

Company: I-Medata, Tel Aviv Medical Center (Ichilov)
Location: Tel Aviv, Israel


About Us: I-Medata is the data science center of Tel Aviv Medical Center, dedicated to pioneering innovative technologies and data-driven solutions in healthcare. We collaborate with global medical organizations and digital health companies to develop AI models and data solutions utilizing EMR data, imaging data, and other relevant information. Our projects seamlessly integrate into TLVMC's clinical workflow, fostering collaboration between data scientists, physicians, and research labs to drive impactful advancements in healthcare.
Position Summary: We seek an experienced Senior Data Scientist to join our team. As a Senior Data Scientist at I-Medata, you will play a critical role in developing advanced clinical Decision Support Systems that have the potential to revolutionize healthcare practices. You will collaborate with a team of skilled researchers and have the opportunity to lead projects that drive innovation in healthcare data science.
Responsibilities:

Develop machine learning models for clinical decision support systems, utilizing structured (EMR database) and unstructured (clinical notes, imaging data) data sources.
Implement end-to-end data pipelines, encompassing data retrieval, cleaning, harmonization, and extracting meaningful clinical features.
Conducted exploratory clinical data analysis and visualization and effectively communicated the results to various stakeholders, including fellow data scientists, hospital clinicians, and management.
Build proof-of-concept (POC) projects from the ground up to quickly evaluate new healthcare data science initiatives.
Lead collaborative projects with digital health companies or research institutions, including defining project scope, priorities, and timelines.




Qualifications:

A Master's or Ph.D. in Computer Science, Data Science, Machine Learning, Biostatistics, Bioinformatics, or a related field is required.
A proven track record with at least ten years of hands-on experience in Data Science, particularly in a healthcare or clinical research environment. This experience should encompass machine learning techniques, statistical analysis, and data modeling proficiency.
Strong programming skills in languages such as Python or R and experience using relevant libraries and frameworks for data analysis and modeling are essential.
A demonstrated ability to conduct research, including designing experiments, conducting comprehensive literature reviews, and applying concepts and findings from the literature.
Clinical and biological data experience is advantageous
Familiarity with healthcare-related datasets is advantageous.
Experience in Natural Language Processing (NLP) and image processing would be an advantage
Benefits:

· Competitive salary and benefits package.
· Opportunity to work on cutting-edge healthcare data science projects.
· Collaborative and innovative work environment.
· Access to the resources and expertise of Tel Aviv Medical Center.
"""

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
    expected_json = get_expected_cv_data("position.json")
    json_format = get_compliation(
        system_message=f"""
                Extract the Position into the following format:
                {json.dumps(expected_json,indent=4)}
                """,
        user_input=user_input,
        api_key=os.environ["OPENAI_API_KEY"],
    )

    user_extracted_data = json.loads(json_format.choices[0].message.content)
    set_user_cv_data(
        user_json_filename="user_position.json", user_cv_user=user_extracted_data
    )
