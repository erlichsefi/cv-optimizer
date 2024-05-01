import json
import os
import shutil
import subprocess


def get_cv_blueprint():
    with open("blueprints/cv.json", "r") as file:
        return json.load(file)


def get_data_from_pdf(filename):
    from PyPDF2 import PdfReader
    if isinstance(filename,str):
        text = ""
        with open(filename, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
        return text
    else:
        from tempfile import NamedTemporaryFile
        from PyPDF2 import PdfReader

        with NamedTemporaryFile(dir=".", suffix=".pdf") as f:
            f.write(filename.getbuffer())

            text = ""
            with open(f.name, "rb") as f:
                reader = PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text()
            return text
        

    
def set_user_extract_cv_data(user_cv_data):
    with open("user_data/user_extracted_cv.json", "w") as file:
        return json.dump(user_cv_data, file)
    
def get_user_extract_cv_data():
    with open("user_data/user_extracted_cv.json", "r") as file:
        return json.load(file)

# 
def set_completed_cv_data(user_cv_data):
    if os.path.exists("user_data/user_completed_cv.json"):
        with open("user_data/user_completed_cv.json", "r") as file:
            complete = json.load(file)
    else:
        complete = {}
    complete[get_datetime_str()] = user_cv_data
    with open("user_data/user_completed_cv.json", "w") as file:
        return json.dump(complete, file)
    
def get_completed_cv_data():
    with open("user_data/user_completed_cv.json", "r") as file:
        complete = json.load(file)
        return complete[max(complete.keys(),key=lambda x:str_to_datetime(x))]

def get_cache_key():
    from datetime import datetime

    current_datetime = datetime.now()
    return current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

def get_datetime_str():
    from datetime import datetime

    current_datetime = datetime.now()
    return current_datetime.strftime("%Y-%m-%d-%H-%M-%S")

def str_to_datetime(date_string):
    from datetime import datetime

    return datetime.strptime(date_string, "%Y-%m-%d-%H-%M-%S")




def cache_chat(message,cache_key):
    with open(f"user_data/cache_message_{cache_key}.json", "w") as file:
        return json.dump(message, file)
    
def set_drill_down_communiation(drill_down):
    with open("user_data/user_drill_down.json", "w") as file:
        return json.dump(drill_down, file)
    

def get_position_blueprint():
    with open("blueprints/position.json", "r") as file:
        return json.load(file)
    

def set_position_data(user_position_data):
    with open("user_data/user_position.json", "w") as file:
        return json.dump(user_position_data, file)
    
def get_position_data():
    with open("user_data/user_position.json", "r") as file:
        return json.load(file)

def set_position_cv_offers(list_of_cvs_options):
    with open(f"user_data/user_position_cv_offers.json", "w") as file:
            json.dump(list_of_cvs_options,file)
        

def get_all_position_cv_offers():
    with open(f"user_data/user_position_cv_offers.json", "r") as file:
        return json.load(file)
    
    
def get_expected_latex_format():
    with open("cv.tex", "r") as file:
        return file.read()

def set_user_latex_file(user_latex,extract_latex=False):

    if extract_latex:
        string = user_latex.choices[0].message.content
        user_latex = string.split("```latex")[1].split("```")[0]

    with open("user_data/user_tex.tex", "w") as file:
        file.write(user_latex)


def compile_user_latex():
    tex_filename = "user_data/user_tex.tex"
    filename, _ = os.path.splitext(tex_filename)
    # the corresponding PDF filename
    pdf_filename = filename + ".pdf"

    # compile TeX file
    # brew install basictex
    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", tex_filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # check if PDF is successfully generated
    if not os.path.exists(pdf_filename):
        error_message  = "process output:" + result.stdout.decode().split("Runaway argument?")[1]
        raise RuntimeError(f"PDF output not found. Error message: {error_message}")
    return pdf_filename

def get_user_latex_file():
    with open("user_data/user_tex.tex", "r") as file:
        return file.read()
    
def move_pdf_to_created():
    # Copy source file to destination file
    pdf_path = "user_data/user_tex.tex"

    position_folder = "user_data/position_cv"
    if not os.path.exists(position_folder):
        os.makedirs(position_folder)

    index = len(os.listdir(position_folder))
    pdf_path = "user_data/user_tex.pdf"
    offer_path = f"{position_folder}/offer_{index}"
    shutil.copy(pdf_path, offer_path)

    return offer_path



