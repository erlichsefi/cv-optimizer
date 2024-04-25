import json


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
    with open("user_data/user_completed_cv.json", "w") as file:
        return json.dump(user_cv_data, file)
    
def get_completed_cv_data():
    with open("user_data/user_completed_cv.json", "r") as file:
        return json.load(file)


def set_drill_down_communiation(drill_down):
    with open("user_data/user_drill_down.json", "w") as file:
        return json.dump(drill_down, file)
    
def get_position_blueprint():
    with open("blueprints/position.json", "r") as file:
        return json.load(file)
    

def set_position_data(user_position_data):
    with open("user_data/user_position.json", "w") as file:
        return json.dump(user_position_data, file)
