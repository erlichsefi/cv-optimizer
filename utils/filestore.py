import json
import os


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
    for index,cv in enumerate(list_of_cvs_options):
        set_position_cv_offer(cv,index)
        
def set_position_cv_offer(cv,index):
    with open(f"user_data/user_position_cv_offer_{index}.json", "w") as file:
        json.dump(cv,file)