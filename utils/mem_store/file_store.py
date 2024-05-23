import json
import os
import shutil
from .base_store import StateStore


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
    def presist_compliation(cls, messages, generations, model, cache_key=None):
        if not cache_key:
            cache_key = cls.get_cache_key()

        exsiting = {}
        if os.path.exists("user_data/compliations.json"):
            with open("user_data/compliations.json", "r") as file:
                exsiting = json.load(file)

        exsiting[cache_key] = {
            "messages": messages,
            "generations": generations,
            "model": model,
        }

        # dump
        with open("user_data/compliations.json", "w") as file:
            json.dump(exsiting, file)

    @classmethod
    def get_presist_compliation(cls):
        with open("user_data/compliations.json", "r") as file:
            return json.load(file)

    #
    @classmethod
    def set_user_extract_cv_data(cls, user_cv_data, pdf_path):
        with open("user_data/user_extracted_cv.json", "w") as file:
            _pdf_path = cls.get_upload_file_name(pdf_path)
            return json.dump({"data":user_cv_data,"filename":_pdf_path}, file)

    @classmethod
    def unset_user_extract_cv_data(cls):
        os.remove("user_data/user_extracted_cv.json")

    @classmethod
    def has_user_extract_cv_data(cls):
        return os.path.exists("user_data/user_extracted_cv.json")

    @classmethod
    def get_user_extract_cv_data(cls):
        with open("user_data/user_extracted_cv.json", "r") as file:
            return json.load(file)['data']
        
    @classmethod
    def get_user_extract_cv_file_name(cls):
        with open("user_data/user_extracted_cv.json", "r") as file:
            return json.load(file)['filename']

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
    def set_chain_messages(cls, id, chat_about_extracted_cv, closed=False, **kwarg):
        with open(f"user_data/chain_message_on_{id}.json", "w") as file:
            json.dump({"data": chat_about_extracted_cv, "closed": closed}, file)

    @classmethod
    def has_chain_messages(cls, id, closed=False, **kwrg):
        if not os.path.exists(f"user_data/chain_message_on_{id}.json"):
            return False

        with open(f"user_data/chain_message_on_{id}.json", "r") as file:
            return json.load(file)["closed"] == closed

    @classmethod
    def get_chain_messages(cls, id):
        if cls.has_chain_messages(id):
            with open(f"user_data/chain_message_on_{id}.json", "r") as file:
                return json.load(file)["data"]
        else:
            return []

    @classmethod
    def set_completed_cv_data(cls, user_cv_data):
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
            return complete[max(complete.keys(), key=lambda x: cls.str_to_datetime(x))]

    #

    @classmethod
    def set_drill_down_communiation(cls, drill_down):
        with open("user_data/user_drill_down.json", "w") as file:
            return json.dump(drill_down, file)

    #
    @classmethod
    def set_position_data(cls, position_name, user_position_data):
        if not os.path.exists("user_data/user_position.json"):
            exiting = {}
        else:
            with open("user_data/user_position.json", "r") as file:
                exiting = json.load(file)
            exiting[position_name] = user_position_data
        with open("user_data/user_position.json", "w") as file:
                json.dump(exiting,file)

    @classmethod
    def has_position_data(cls,position_name=None):
        if not os.path.exists("user_data/user_position.json"):
            return False
        elif position_name:
            return cls.get_position_data(position_name) != None
        else:
            return True

    @classmethod
    def get_position_data(cls,position_name=None):
        with open("user_data/user_position.json", "r") as file:
            response = json.load(file)

            if position_name:
                return response.get(position_name,None)
            return response


    #
    @classmethod
    def set_position_cv_offers(cls,list_of_cvs_options,current_conversation):
        existing = {}
        if os.path.exists("user_data/user_position_cv_offers.json"):
            with open(f"user_data/user_position_cv_offers.json", "r") as file:
                existing = json.load(file)

        existing[current_conversation] =  list_of_cvs_options if isinstance(list_of_cvs_options,list) else [list_of_cvs_options]
        with open(f"user_data/user_position_cv_offers.json", "w") as file:
            json.dump(existing, file)

    @classmethod
    def has_position_cv_offers(cls,current_conversation):
        if not os.path.exists("user_data/user_position_cv_offers.json"):
            return False
        with open(f"user_data/user_position_cv_offers.json", "r") as file:
            return current_conversation in json.load(file)

    @classmethod
    def get_all_position_cv_offers(cls,current_conversation):
        with open(f"user_data/user_position_cv_offers.json", "r") as file:
            return json.load(file)[current_conversation]

    #
    @classmethod
    def set_identified_gap_from_hiring_team(cls, gaps_to_adresss):
        with open(f"user_data/identified_gap_from_hiring_team.json", "w") as file:
            json.dump(gaps_to_adresss, file)

    @classmethod
    def has_identified_gap_from_hiring_team(cls):
        return os.path.exists("user_data/identified_gap_from_hiring_team.json")

    @classmethod
    def get_identified_gap_from_hiring_team(cls):
        with open(f"user_data/identified_gap_from_hiring_team.json", "r") as file:
            return json.load(file)

    #

    @classmethod
    def set_base_optimized(cls, user_cv, gen_id):
        if os.path.exists("user_data/base_optimized.json"):
            with open(f"user_data/base_optimized.json", "r") as file:
                content = json.load(file)
        else:
            content = {}

        content[gen_id] = user_cv
        with open(f"user_data/base_optimized.json", "w") as file:
            json.dump(content, file)

    @classmethod
    def has_optimized_cv(cls, gen_id):
        if not os.path.exists("user_data/base_optimized.json"):
            return False
        with open(f"user_data/base_optimized.json", "r") as file:
            return gen_id in json.load(file)

    @classmethod
    def get_base_optimized(cls, gen_id):
        with open(f"user_data/base_optimized.json", "r") as file:
            return json.load(file)[gen_id]

    @classmethod
    def set_issues_to_solve_in_chat(cls, issues_to_solve, gen_id):
        if os.path.exists("user_data/issues_to_solve_in_chat.json"):
            with open(f"user_data/issues_to_solve_in_chat.json", "r") as file:
                content = json.load(file)
        else:
            content = {}

        content[gen_id] = issues_to_solve
        with open(f"user_data/issues_to_solve_in_chat.json", "w") as file:
            json.dump(content, file)

    @classmethod
    def get_issues_to_solve_in_chat(cls, gen_id):
        with open(f"user_data/issues_to_solve_in_chat.json", "r") as file:
            return json.load(file)[gen_id]

    #

    def set_pdfs_files(cls, pdf, current_conversation):
        existing = {}
        if os.path.exists("user_data/pdf_paths.json"):
            with open(f"user_data/pdf_paths.json", "r") as file:
                existing =  json.load(file)
        existing[current_conversation] = pdf

        with open(f"user_data/pdf_paths.json", "w") as file:
            return json.dump(existing,file)
        
    def has_pdfs_files(cls,current_conversation):
        if not os.path.exists("user_data/pdf_paths.json"):
            return False
        
        with open(f"user_data/pdf_paths.json", "r") as file:
            return current_conversation in json.load(file)

    def get_pdfs_files(cls,current_conversation):
        with open(f"user_data/pdf_paths.json", "r") as file:
            return json.load(file)[current_conversation]
    #

    @classmethod
    def wrap_up(cls, complete_path, messages):
        complete_data = {
            "message": messages,
            "extracted_cv": cls.get_user_extract_cv_data(),
            "completed_cv": cls.get_completed_cv_data(),
            "position_data": cls.get_position_data(),
            "offers": cls.get_all_position_cv_offers(),
            "all_compliation": cls.get_presist_compliation(),
        }
        with open(complete_path, "w") as file:
            json.dump(complete_data, file)

        shutil.rmtree("user_data")
        os.mkdir("user_data")
