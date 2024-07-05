from abc import ABC, abstractmethod
import streamlit as st
import os, shutil
import subprocess
import uuid
import json
import cv


def move_pdf_to_created(position_folder):
    # Copy source file to destination file
    pdf_path = ".tex/user_tex.pdf"

    # to where
    if not os.path.exists(position_folder):
        os.makedirs(position_folder)

    index = len(os.listdir(position_folder))

    offer_path = os.path.join(position_folder, f"offer_{index}.pdf")
    shutil.copy(pdf_path, os.path.join(position_folder, f"offer_{index}.pdf"))

    return offer_path


class StateStore(ABC):

    def __init__(self, resources_dir):
        self.resources_dir = resources_dir
        self.user_tex_path = os.path.join(resources_dir, "user_data/user_tex.tex")
        self.positions_dir_cv = os.path.join(resources_dir, "user_data/position_cv")
        self.blueprint_dir = os.path.join(resources_dir,"blueprints")

    def _blueprint_path_to(self, file_name):
        return os.path.join(self.blueprint_dir, file_name)
    
    def get_cv_blueprint(self):
        return cv.get_templete_for_prompt()

    def get_position_blueprint(self):
        with open(self._blueprint_path_to("position.json"), "r") as file:
            return json.load(file)

    def get_expected_latex_format(self):
        with open(self._blueprint_path_to("cv.tex"), "r") as file:
            return file.read()
        
    def get_upload_file_name(self, pdf_path):
        if isinstance(pdf_path, st.runtime.uploaded_file_manager.UploadedFile):
            return pdf_path.name
        return pdf_path

    def get_cache_key(self):
        from datetime import datetime

        current_datetime = datetime.now()
        return current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

    @abstractmethod
    def presist_compliation(self, messages, generations, model, cache_key=None):
        pass

    @abstractmethod
    def get_presist_compliation(self):
        pass

    @abstractmethod
    def set_user_extract_cv_data(self, user_cv_data, pdf_path):
        pass

    @abstractmethod
    def unset_user_extract_cv_data(self):
        pass

    @abstractmethod
    def get_user_extract_cv_file_name(self):
        pass

    @abstractmethod
    def has_user_extract_cv_data(self):
        pass

    @abstractmethod
    def get_user_extract_cv_data(self):
        pass

    @abstractmethod
    def set_issues_to_overcome(self, issues_found):
        pass

    @abstractmethod
    def has_issues_to_overcome(self):
        pass

    @abstractmethod
    def get_issues_to_overcome(self):
        pass

    @abstractmethod
    def set_chain_messages(self, id, chat_about_extracted_cv):
        pass

    @abstractmethod
    def has_chain_messages(self, id, **kwrg):
        pass

    @abstractmethod
    def get_chain_messages(self, id, closed=True):
        pass

    @abstractmethod
    def set_completed_cv_data(self, user_cv_data):
        pass

    @abstractmethod
    def has_completed_cv_data(self):
        pass

    @abstractmethod
    def get_completed_cv_data(self):
        pass

    def get_datetime_str(self):
        from datetime import datetime

        current_datetime = datetime.now()
        return current_datetime.strftime("%Y-%m-%d-%H-%M-%S")

    def str_to_datetime(self, date_string):
        from datetime import datetime

        return datetime.strptime(date_string, "%Y-%m-%d-%H-%M-%S")

    @abstractmethod
    def set_drill_down_communiation(self, drill_down):
        pass

    @abstractmethod
    def set_position_data(self, position_name, user_position_data):
        pass

    @abstractmethod
    def has_position_data(self, position_name=None):
        pass

    @abstractmethod
    def get_position_data(self, position_name=None):
        pass

    @abstractmethod
    def set_position_cv_offers(self, list_of_cvs_options, current_conversation):
        pass

    @abstractmethod
    def has_position_cv_offers(self, current_conversation):
        pass

    @abstractmethod
    def has_identified_gap_from_hiring_team(self):
        pass

    @abstractmethod
    def has_optimized_cv(self, en_id):
        pass

    @abstractmethod
    def set_identified_gap_from_hiring_team(self, gaps_to_adresss):
        pass

    @abstractmethod
    def get_identified_gap_from_hiring_team(self):
        pass

    @abstractmethod
    def set_base_optimized(self, user_cv, gen_id):
        pass

    @abstractmethod
    def get_base_optimized(self, gen_id):
        pass

    @abstractmethod
    def set_issues_to_solve_in_chat(self, issues_to_solve, gen_id):
        pass

    @abstractmethod
    def get_issues_to_solve_in_chat(self, gen_id):
        pass

    @abstractmethod
    def get_all_position_cv_offers(self, current_conversation):
        pass

    @abstractmethod
    def get_all_position_cv_cover_letters(self, current_conversation):
        pass

    #

    @abstractmethod
    def set_pdfs_files(self, pdf, current_conversation):
        pass

    @abstractmethod
    def has_pdfs_files(self, current_conversation):
        pass

    @abstractmethod
    def get_pdfs_files(self, current_conversation):
        pass

    def set_user_latex_file(self, user_latex):
        user_latex = user_latex.replace("```latex", "").replace("```", "")
        with open(self.user_tex_path, "w") as file:
            file.write(user_latex)

    def compile_user_latex(self):
        tex_temp_folder = ".tex"
        filename, _ = os.path.splitext(self.user_tex_path)
        # the corresponding PDF filename
        pdf_filename = (
            os.path.join(tex_temp_folder, os.path.split(filename)[-1]) + ".pdf"
        )

        # compile TeX file
        # brew install basictex
        if os.path.exists(tex_temp_folder):
            shutil.rmtree(tex_temp_folder)
        os.mkdir(tex_temp_folder)

        result = subprocess.run(
            [
                "pdflatex",
                "-interaction=nonstopmode",
                "-output-directory=.tex",
                self.user_tex_path,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # check if PDF is successfully generated
        if not os.path.exists(pdf_filename):
            error_message = "process output:" + result.stdout.decode()
            raise RuntimeError(f"PDF output not found. Error message: {error_message}")
        return pdf_filename

    def get_user_latex_file(self):
        with open(self.user_tex_path, "r") as file:
            return file.read()

    def move_pdf_to_created(self):
        # Copy source file to destination file
        pdf_path = ".tex/user_tex.pdf"

        # to where
        if not os.path.exists(self.positions_dir_cv):
            os.makedirs(self.positions_dir_cv)

        index = str(uuid.uuid4())

        offer_path = os.path.join(self.positions_dir_cv, f"offer_{index}.pdf")
        shutil.copy(pdf_path, os.path.join(self.positions_dir_cv, f"offer_{index}.pdf"))

        return offer_path

    @abstractmethod
    def wrap_up(self, complete_path, messages):
        pass
