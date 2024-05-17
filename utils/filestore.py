import json
import os
import shutil
import subprocess
from abc import ABC, abstractmethod
import streamlit as st

def extract_1(filename):
    from pdfminer.high_level import extract_text

    return extract_text(filename)


def extract_2(filename):
    #from PyPDF2 import PdfReader
    from pypdf import PdfReader
    text = ""
    with open(filename, "rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text



        

class StateStore(ABC):

    @classmethod
    def get_data_from_pdf(cls,filename):

        extract_1(filename)

        if isinstance(filename,str):
            return extract_1(filename)
        else:
            from tempfile import NamedTemporaryFile
            with NamedTemporaryFile(dir=".", suffix=".pdf") as f:
                f.write(filename.getbuffer())
                return extract_1(f.name)
            
    @classmethod
    @abstractmethod
    def get_cv_blueprint(cls):
        pass

    @classmethod
    @abstractmethod
    def get_position_blueprint(cls):
        pass

    @classmethod
    @abstractmethod
    def get_expected_latex_format(cls):
        pass
    
    @classmethod
    def get_cache_key(cls):
        from datetime import datetime

        current_datetime = datetime.now()
        return current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

    @classmethod
    @abstractmethod
    def presist_compliation(cls, messages, generations, model, cache_key=None):
        pass

    @classmethod
    @abstractmethod
    def get_presist_compliation(cls):
        pass

    @classmethod
    @abstractmethod
    def set_user_extract_cv_data(cls, user_cv_data):
        pass

    @classmethod
    @abstractmethod
    def has_user_extract_cv_data(cls):
        pass

    @classmethod
    @abstractmethod
    def get_user_extract_cv_data(cls):
        pass

    @classmethod
    @abstractmethod
    def set_issues_to_overcome(cls, issues_found):
        pass

    @classmethod
    @abstractmethod
    def has_issues_to_overcome(cls):
        pass

    @classmethod
    @abstractmethod
    def get_issues_to_overcome(cls):
        pass


    @classmethod
    @abstractmethod
    def set_chain_messages(cls, id, chat_about_extracted_cv):
        pass

    @classmethod
    @abstractmethod
    def has_chain_messages(cls,id, **kwrg):
        pass

    @classmethod
    @abstractmethod
    def get_chain_messages(cls,id):
        pass
    
    
    @classmethod
    @abstractmethod
    def set_completed_cv_data(cls, user_cv_data):
        pass

    @classmethod
    @abstractmethod
    def has_completed_cv_data(cls):
        pass
    
    @classmethod
    @abstractmethod
    def get_completed_cv_data(cls):
        pass

    @classmethod
    def get_datetime_str(cls):
        from datetime import datetime

        current_datetime = datetime.now()
        return current_datetime.strftime("%Y-%m-%d-%H-%M-%S")

    @classmethod
    def str_to_datetime(cls,date_string):
        from datetime import datetime

        return datetime.strptime(date_string, "%Y-%m-%d-%H-%M-%S")
    @classmethod
    @abstractmethod
    def set_drill_down_communiation(cls, drill_down):
        pass

    @classmethod
    @abstractmethod
    def set_position_data(cls, user_position_data):
        pass
    
    @classmethod
    @abstractmethod
    def has_position_data(cls):
        pass
    
    @classmethod
    @abstractmethod
    def get_position_data(cls):
        pass

    @classmethod    
    @abstractmethod
    def set_position_cv_offers(cls, list_of_cvs_options):
        pass

    @classmethod
    @abstractmethod
    def has_position_cv_offers(cls):
        pass
    
    @classmethod
    @abstractmethod
    def get_all_position_cv_offers(cls):
        pass

    @classmethod
    @abstractmethod
    def set_user_latex_file(cls, user_latex):
        pass

    @classmethod
    @abstractmethod
    def compile_user_latex(cls):
        pass

    @classmethod
    @abstractmethod
    def get_user_latex_file(cls):
        pass
    
    @classmethod       
    @abstractmethod
    def move_pdf_to_created(cls):
        pass

    @classmethod
    @abstractmethod
    def wrap_up(cls, complete_path, messages):
        pass



class  StermlitStateStore(StateStore):

    @classmethod
    def get_cv_blueprint(cls):
        with open("blueprints/cv.json", "r") as file:
            return json.load(file)

    @classmethod
    def get_position_blueprint(cls):
        with open("blueprints/position.json", "r") as file:
            return json.load(file)

    @classmethod
    def get_expected_latex_format(cls):
        with open("blueprints/cv.tex", "r") as file:
            return file.read() 

    @classmethod
    def presist_compliation(cls,messages,generations,model,cache_key=None):
        if  not cache_key:
            cache_key = cls.get_cache_key()

        exsiting = {}
        if os.path.exists("user_data/compliations.json"):
            with open("user_data/compliations.json", "r") as file:
                exsiting = json.load(file)

        exsiting[cache_key] = {
            "messages":messages,
            "generations":generations,
            "model":model
        }
    
        # dump
        with open("user_data/compliations.json", "w") as file:
            json.dump(exsiting,file)

    
    @classmethod
    def get_presist_compliation(cls):
        with open("user_data/compliations.json", "r") as file:
            return json.load(file)

    #
    @classmethod
    def set_user_extract_cv_data(cls,user_cv_data):
        st.session_state["user_extracted_cv"] = user_cv_data

    @classmethod  
    def has_user_extract_cv_data(cls):
        return "user_extracted_cv" in st.session_state

        
    @classmethod 
    def get_user_extract_cv_data(cls):
        if cls.has_user_extract_cv_data():
            return st.session_state["user_extracted_cv"]
    #
        
    @classmethod
    def set_issues_to_overcome(cls, issues_found):
        st.session_state["issues_to_overcome"] = issues_found

    @classmethod
    def has_issues_to_overcome(cls):
        return "issues_to_overcome" in st.session_state

    @classmethod
    def get_issues_to_overcome(cls):
        if cls.has_issues_to_overcome():
            return st.session_state["issues_to_overcome"]


    @classmethod
    def set_chain_messages(cls, id, chat_about_extracted_cv,closed=False,**kwarg):
        st.session_state[f"chain_message_on_{id}"] = {
            "data":chat_about_extracted_cv,
            "closed":closed
        }
    @classmethod
    def has_chain_message_on_extracted_cv(cls,id,closed=False,**kwrg):
        return f'chain_message_on_{id}' in st.session_state and  st.session_state[f'chain_message_on_{id}']['closed'] == closed

    @classmethod
    def get_chain_message_on_extracted_cv(cls,id):
        if cls.has_chain_message_on_extracted_cv(id):
            return st.session_state[f"chain_message_on_{id}"]['data']
    # 
    @classmethod
    def set_completed_cv_data(cls,user_cv_data):
        if "user_completed_cv" in st.session_state:
            complete = st.session_state["user_completed_cv"] 
        else:
            complete = {}
        complete[cls.get_datetime_str()] = user_cv_data
        st.session_state["user_completed_cv"] = complete

    @classmethod
    def has_completed_cv_data(cls):
        return "user_completed_cv" in st.session_state
    
    @classmethod
    def get_completed_cv_data(cls):
        complete = st.session_state["user_completed_cv"] 
        return complete[max(complete.keys(),key=lambda x:cls.str_to_datetime(x))]

    #
    @classmethod
    def set_drill_down_communiation(cls,drill_down):
        st.session_state["user_drill_down"] = drill_down
        
    # 
    @classmethod
    def set_position_data(cls,user_position_data):
        st.session_state["user_position"] = user_position_data

        
    @classmethod
    def has_position_data(cls):
        return "user_position" in st.session_state
    
    @classmethod
    def get_position_data(cls):
        return st.session_state['user_position']
    #
    @classmethod    
    def set_position_cv_offers(cls,list_of_cvs_options):
        st.session_state['user_position_cv_offers'] = list_of_cvs_options

    @classmethod
    def has_position_cv_offers(cls):
        return "user_position_cv_offers" in st.session_state
    
    @classmethod
    def get_all_position_cv_offers(cls):
        return st.session_state['user_position_cv_offers']
    #

    @classmethod
    def set_user_latex_file(cls,user_latex):
        user_latex = user_latex.split("```latex")[1].split("```")[0]
        with open("user_data/user_tex.tex", "w") as file:
            file.write(user_latex)

    @classmethod
    def compile_user_latex(cls):
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

    @classmethod
    def get_user_latex_file(cls):
        with open("user_data/user_tex.tex", "r") as file:
            return file.read()
    
    @classmethod       
    def move_pdf_to_created(cls):
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


    @classmethod
    def wrap_up(cls,complete_path,messages):
        complete_data = {
            "message":messages,
            "extracted_cv":cls.get_user_extract_cv_data(),
            "completed_cv":cls.get_completed_cv_data(),
            "position_data":cls.get_position_data(),
            "offers":cls.get_all_position_cv_offers(),
            "all_compliation":cls.get_presist_compliation()
        }
        with open(complete_path, "w") as file:
            json.dump(complete_data,file)

        shutil.rmtree("user_data")
        os.mkdir("user_data")



class FileStateStore(StateStore):

    @classmethod
    def get_cv_blueprint(cls):
        with open("blueprints/cv.json", "r") as file:
            return json.load(file)

    @classmethod
    def get_position_blueprint(cls):
        with open("blueprints/position.json", "r") as file:
            return json.load(file)

    @classmethod
    def get_expected_latex_format(cls):
        with open("blueprints/cv.tex", "r") as file:
            return file.read()
    
        
    @classmethod
    def presist_compliation(cls,messages,generations,model,cache_key=None):
        if  not cache_key:
            cache_key = cls.get_cache_key()

        exsiting = {}
        if os.path.exists("user_data/compliations.json"):
            with open("user_data/compliations.json", "r") as file:
                exsiting = json.load(file)

        exsiting[cache_key] = {
            "messages":messages,
            "generations":generations,
            "model":model
        }
    
        # dump
        with open("user_data/compliations.json", "w") as file:
            json.dump(exsiting,file)

    
    @classmethod
    def get_presist_compliation(cls):
        with open("user_data/compliations.json", "r") as file:
            return json.load(file)

    #
    @classmethod
    def set_user_extract_cv_data(cls,user_cv_data):
        with open("user_data/user_extracted_cv.json", "w") as file:
            return json.dump(user_cv_data, file)

    @classmethod  
    def has_user_extract_cv_data(cls):
        return os.path.exists("user_data/user_extracted_cv.json")

    @classmethod 
    def get_user_extract_cv_data(cls):
        with open("user_data/user_extracted_cv.json", "r") as file:
            return json.load(file)

    # 
        
    @classmethod
    def set_issues_to_overcome(cls, issues_found):
        with open("user_data/issues_to_overcome.json", "w") as file:
            json.dump(issues_found, file)

    @classmethod
    def has_issues_to_overcome(cls):
        return os.path.exists("user_data/issues_to_overcome.json")

    @classmethod
    def get_issues_to_overcome(cls):
        with open("user_data/issues_to_overcome.json", "r") as file:
            return json.load(file)

    @classmethod
    def set_chain_messages(cls,id, chat_about_extracted_cv,closed=False,**kwarg):
        with open(f"user_data/chain_message_on_{id}.json", "w") as file:
            json.dump({
            "data":chat_about_extracted_cv,
            "closed":closed
        }, file)

    @classmethod
    def has_chain_messages(cls,id,closed=False,**kwrg):
        if not os.path.exists(f"user_data/chain_message_on_{id}.json"):
            return False
        
        with open(f"user_data/chain_message_on_{id}.json", "r") as file:
            return json.load(file)['closed'] == closed

    @classmethod
    def get_chain_message(cls,id):
        if cls.has_chain_message_on_extracted_cv(id):
            with open(f"user_data/chain_message_on_{id}.json", "r") as file:
                return json.load(file)['data']
        else:
            return []
        
        
    @classmethod
    def set_completed_cv_data(cls,user_cv_data):
        if os.path.exists("user_data/user_completed_cv.json"):
            with open("user_data/user_completed_cv.json", "r") as file:
                complete = json.load(file)
        else:
            complete = {}
        complete[cls.get_datetime_str()] = user_cv_data
        with open("user_data/user_completed_cv.json", "w") as file:
            return json.dump(complete, file)

    @classmethod
    def has_completed_cv_data(cls):
        return os.path.exists("user_data/user_completed_cv.json")
    
    @classmethod
    def get_completed_cv_data(cls):
        with open("user_data/user_completed_cv.json", "r") as file:
            complete = json.load(file)
            return complete[max(complete.keys(),key=lambda x:cls.str_to_datetime(x))]

    #


    @classmethod
    def set_drill_down_communiation(cls,drill_down):
        with open("user_data/user_drill_down.json", "w") as file:
            return json.dump(drill_down, file)
        
    # 
    @classmethod
    def set_position_data(cls,user_position_data):
        with open("user_data/user_position.json", "w") as file:
            return json.dump(user_position_data, file)
        
    @classmethod
    def has_position_data(cls):
        return os.path.exists("user_data/user_position.json")
    
    @classmethod
    def get_position_data(cls):
        with open("user_data/user_position.json", "r") as file:
            return json.load(file)
    #
    @classmethod    
    def set_position_cv_offers(cls,list_of_cvs_options):
        with open(f"user_data/user_position_cv_offers.json", "w") as file:
                json.dump(list_of_cvs_options,file)

    @classmethod
    def has_position_cv_offers(cls):
        return os.path.exists("user_data/user_position_cv_offers.json")
    
    @classmethod
    def get_all_position_cv_offers(cls):
        with open(f"user_data/user_position_cv_offers.json", "r") as file:
            return json.load(file)
    #

    @classmethod
    def set_user_latex_file(cls,user_latex):
        user_latex = user_latex.split("```latex")[1].split("```")[0]
        with open("user_data/user_tex.tex", "w") as file:
            file.write(user_latex)

    @classmethod
    def compile_user_latex(cls):
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

    @classmethod
    def get_user_latex_file(cls):
        with open("user_data/user_tex.tex", "r") as file:
            return file.read()
    
    @classmethod       
    def move_pdf_to_created(cls):
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


    @classmethod
    def wrap_up(cls,complete_path,messages):
        complete_data = {
            "message":messages,
            "extracted_cv":cls.get_user_extract_cv_data(),
            "completed_cv":cls.get_completed_cv_data(),
            "position_data":cls.get_position_data(),
            "offers":cls.get_all_position_cv_offers(),
            "all_compliation":cls.get_presist_compliation()
        }
        with open(complete_path, "w") as file:
            json.dump(complete_data,file)

        shutil.rmtree("user_data")
        os.mkdir("user_data")


