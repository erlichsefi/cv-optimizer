import os
import json
import platform
import subprocess
from openai import OpenAI


def get_user_cv_data(user_json_filename):
    with open(user_json_filename,"r") as file:
        return json.load(file)

def get_expected_latex_format(tex_filename):
    with open(tex_filename,"r") as file:
        return file.read()
    
def get_user_latex_file(tex_filename):
    with open(tex_filename,"r") as file:
        return file.read()

def dump_latex_to_file(user_latex,user_latex_filename):
    with open(user_latex_filename,"w") as file:
        file.write(user_latex)
    
def get_compliation(system_message,user_input,api_key):
    client = OpenAI(api_key=api_key)
    stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=
            [
             {"role":"system", "content": system_message},
             {"role":"user", "content": user_input}
           
            ],
            stream=False,
        )
    return stream

def compile_latex(tex_filename):
    filename, _ = os.path.splitext(tex_filename)
    # the corresponding PDF filename
    pdf_filename = filename + '.pdf'

    # compile TeX file
    # brew install basictex
    result = subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_filename], stderr=subprocess.PIPE)

    # check if PDF is successfully generated
    if not os.path.exists(pdf_filename):
        error_message = result.stderr.decode('utf-8').strip()
        raise RuntimeError(f'PDF output not found. Error message: {error_message}')

    

if __name__ == "__main__":

    user_cv_data = get_user_cv_data("user_csv.json")
    expected_format = get_expected_latex_format("cv.tex")
    generations = get_compliation(system_message=f"""
                    Give the user data, fill the latex format:
                    {expected_format}

                    make sure the latex is valid.
                    """,
                    user_input=json.dumps(user_cv_data,indent=4),
                    api_key=os.environ['OPENAI_API_KEY'])
    

    dump_latex_to_file(generations.choices[0].message.content,"user_tex.tex")
    for _ in range(3):
        try:
            compile_latex("user_tex.tex")
        except RuntimeError as e:
            latex_file_content = get_user_latex_file("user_tex.tex")
            generations = get_compliation(system_message="""
                    You are tring to complie a latex file
                    fix the issue araise from the compling process
                    """,
                    user_input=f"""
                    {latex_file_content}

                    error is:
                    {e}
                    """,
                    api_key=os.environ['OPENAI_API_KEY'])
            dump_latex_to_file(generations.choices[0].message.content,"user_tex.tex")

    