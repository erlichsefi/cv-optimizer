import json
import os
import shutil
import subprocess
import io


def get_cv_blueprint():
    with open("blueprints/cv.json", "r") as file:
        return json.load(file)

def get_position_blueprint():
    with open("blueprints/position.json", "r") as file:
        return json.load(file)

def get_expected_latex_format():
    with open("blueprints/cv.tex", "r") as file:
        return file.read()
    

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

 #

def get_cache_key():
    from datetime import datetime

    current_datetime = datetime.now()
    return current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
        
def presist_compliation(messages,generations,model,cache_key=None):
    if  not cache_key:
        cache_key = get_cache_key()

    with open("user_data/compliations.json", "a") as file:
        try:
            exsiting =  json.load(file)
        except io.UnsupportedOperation:
            exsiting = {}

        exsiting[cache_key] = {
            "messages":messages,
            "generations":generations,
            "model":model
        }
  


        json.dumps(exsiting)

def get_presist_compliation():
    with open("user_data/compliations.json", "r") as file:
        return json.load(file)

#
def set_user_extract_cv_data(user_cv_data):
    with open("user_data/user_extracted_cv.json", "w") as file:
        return json.dump(user_cv_data, file)
    
def has_user_extract_cv_data():
    return os.path.exists("user_data/user_extracted_cv.json")
    
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

def has_completed_cv_data():
    return os.path.exists("user_data/user_completed_cv.json")

def get_completed_cv_data():
    with open("user_data/user_completed_cv.json", "r") as file:
        complete = json.load(file)
        return complete[max(complete.keys(),key=lambda x:str_to_datetime(x))]

#

def get_datetime_str():
    from datetime import datetime

    current_datetime = datetime.now()
    return current_datetime.strftime("%Y-%m-%d-%H-%M-%S")

def str_to_datetime(date_string):
    from datetime import datetime

    return datetime.strptime(date_string, "%Y-%m-%d-%H-%M-%S")


    
def set_drill_down_communiation(drill_down):
    with open("user_data/user_drill_down.json", "w") as file:
        return json.dump(drill_down, file)
    
# 
def set_position_data(user_position_data):
    with open("user_data/user_position.json", "w") as file:
        return json.dump(user_position_data, file)
    
def has_position_data():
    return os.path.exists("user_data/user_position.json")

def get_position_data():
    with open("user_data/user_position.json", "r") as file:
        return json.load(file)
#
def set_position_cv_offers(list_of_cvs_options):
    with open(f"user_data/user_position_cv_offers.json", "w") as file:
            json.dump(list_of_cvs_options,file)

def has_position_cv_offers():
    return os.path.exists("user_data/user_position_cv_offers.json")

def get_all_position_cv_offers():
    with open(f"user_data/user_position_cv_offers.json", "r") as file:
        return json.load(file)
#

def set_user_latex_file(user_latex,extract_latex=False):
    if extract_latex:
        string = user_latex.choices[0].message.content
        user_latex = string.split("```latex")[1].split("```")[0]

    with open("user_data/user_tex.tex", "w") as file:
        file.write(user_latex)


def compile_user_latex():
    tex_filename = "user_data/user_tex.tex"
    tex_temp_folder = ".tex"
    filename, _ = os.path.splitext(tex_filename)
    # the corresponding PDF filename
    pdf_filename = os.path.join(tex_temp_folder,os.path.split(filename)[-1]) + ".pdf"

    # compile TeX file
    # brew install basictex
    if os.path.exists(tex_temp_folder):
        shutil.rmtree(tex_temp_folder)
    os.mkdir(tex_temp_folder)

    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode","-output-directory=.tex",tex_filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # check if PDF is successfully generated
    if not os.path.exists(pdf_filename):
        error_message  = "process output:" + result.stdout
        raise RuntimeError(f"PDF output not found. Error message: {error_message}")
    return pdf_filename

def get_user_latex_file():
    with open("user_data/user_tex.tex", "r") as file:
        return file.read()
    
def move_pdf_to_created():
    # Copy source file to destination file
    pdf_path = ".tex/user_tex.pdf"

    # to where
    position_folder = "user_data/position_cv"
    if not os.path.exists(position_folder):
        os.makedirs(position_folder)

    index = len(os.listdir(position_folder))
    
    offer_path = os.path.join(position_folder,f"offer_{index}.pdf")
    shutil.copy(pdf_path, os.path.join(position_folder,f"offer_{index}.pdf"))

    return offer_path



def wrap_up(complete_path,messages):
    complete_data = {
        "message":messages,
        "extracted_cv":get_user_extract_cv_data(),
        "completed_cv":get_completed_cv_data(),
        "position_data":get_position_data(),
        "offers":get_all_position_cv_offers(),
        "all_compliation":get_presist_compliation()
    }
    with open(complete_path, "w") as file:
        json.dump(complete_data,file)

    shutil.rmtree("user_data")


