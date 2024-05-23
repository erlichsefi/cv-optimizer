from abc import ABC, abstractmethod
import streamlit as st
import os, shutil
import subprocess


def extract_1(filename):
    from pdfminer.high_level import extract_text

    return extract_text(filename)


def extract_2(filename):
    # from PyPDF2 import PdfReader
    from pypdf import PdfReader

    text = ""
    with open(filename, "rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text


def move_pdf_to_created(cls):
    # Copy source file to destination file
    pdf_path = ".tex/user_tex.pdf"

    # to where
    position_folder = "user_data/position_cv"
    if not os.path.exists(position_folder):
        os.makedirs(position_folder)

    index = len(os.listdir(position_folder))

    offer_path = os.path.join(position_folder, f"offer_{index}.pdf")
    shutil.copy(pdf_path, os.path.join(position_folder, f"offer_{index}.pdf"))

    return offer_path


class StateStore(ABC):

    @classmethod
    def get_data_from_pdf(cls, filename):

        extract_1(filename)

        if isinstance(filename, str):
            return extract_1(filename)
        else:
            from tempfile import NamedTemporaryFile

            with NamedTemporaryFile(dir=".", suffix=".pdf") as f:
                f.write(filename.getbuffer())
                return extract_1(f.name)
    
    @classmethod
    def get_upload_file_name(cls,pdf_path):
        if isinstance(pdf_path,st.runtime.uploaded_file_manager.UploadedFile):
            return pdf_path.name
        return pdf_path

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
    def set_user_extract_cv_data(cls, user_cv_data, pdf_path):
        pass

    @classmethod
    @abstractmethod
    def unset_user_extract_cv_data(cls):
        pass
    
    @classmethod
    @abstractmethod
    def get_user_extract_cv_file_name(cls):
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
    def has_chain_messages(cls, id, **kwrg):
        pass

    @classmethod
    @abstractmethod
    def get_chain_messages(cls, id):
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
    def str_to_datetime(cls, date_string):
        from datetime import datetime

        return datetime.strptime(date_string, "%Y-%m-%d-%H-%M-%S")

    @classmethod
    @abstractmethod
    def set_drill_down_communiation(cls, drill_down):
        pass

    @classmethod
    @abstractmethod
    def set_position_data(cls, position_name, user_position_data):
        pass

    @classmethod
    @abstractmethod
    def has_position_data(cls,position_name=None):
        pass

    @classmethod
    @abstractmethod
    def get_position_data(cls, position_name=None):
        pass

    @classmethod
    @abstractmethod
    def set_position_cv_offers(cls, list_of_cvs_options, current_conversation):
        pass

    @classmethod
    @abstractmethod
    def has_position_cv_offers(cls, current_conversation):
        pass

    @classmethod
    @abstractmethod
    def has_identified_gap_from_hiring_team(cls):
        pass

    @classmethod
    @abstractmethod
    def has_optimized_cv(cls, en_id):
        pass

    @classmethod
    @abstractmethod
    def set_identified_gap_from_hiring_team(cls, gaps_to_adresss):
        pass

    @classmethod
    @abstractmethod
    def get_identified_gap_from_hiring_team(cls):
        pass

    @classmethod
    @abstractmethod
    def set_base_optimized(cls, user_cv, gen_id):
        pass

    @classmethod
    @abstractmethod
    def get_base_optimized(cls, gen_id):
        pass

    @classmethod
    @abstractmethod
    def set_issues_to_solve_in_chat(cls, issues_to_solve, gen_id):
        pass

    @classmethod
    @abstractmethod
    def get_issues_to_solve_in_chat(cls, gen_id):
        pass

    @classmethod
    @abstractmethod
    def get_all_position_cv_offers(cls,current_conversation):
        pass
    #
    @classmethod
    @abstractmethod
    def set_pdfs_files(cls, pdf, current_conversation):
        pass

    @classmethod
    @abstractmethod
    def has_pdfs_files(cls,current_conversation):
        pass
    @classmethod
    @abstractmethod
    def get_pdfs_files(cls,current_conversation):
        pass
    
    @classmethod
    def set_user_latex_file(cls, user_latex):
        user_latex = user_latex.replace("```latex","").replace("```","")
        with open("user_data/user_tex.tex", "w") as file:
            file.write(user_latex)

    @classmethod
    def compile_user_latex(cls):
        tex_filename = "user_data/user_tex.tex"
        tex_temp_folder = ".tex"
        filename, _ = os.path.splitext(tex_filename)
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
                tex_filename,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # check if PDF is successfully generated
        if not os.path.exists(pdf_filename):
            error_message = "process output:" + result.stdout.decode()
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

        offer_path = os.path.join(position_folder, f"offer_{index}.pdf")
        shutil.copy(pdf_path, os.path.join(position_folder, f"offer_{index}.pdf"))

        return offer_path

    @classmethod
    @abstractmethod
    def wrap_up(cls, complete_path, messages):
        pass
