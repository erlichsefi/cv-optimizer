import json
import os
import shutil
from .base_store import StateStore


class FileStateStore(StateStore):

    
    def get_cv_blueprint(self):
        with open("blueprints/cv.json", "r") as file:
            return json.load(file)

    
    def get_position_blueprint(self):
        with open("blueprints/position.json", "r") as file:
            return json.load(file)

    
    def get_expected_latex_format(self):
        with open("blueprints/cv.tex", "r") as file:
            return file.read()

    
    def presist_compliation(self, messages, generations, model, cache_key=None):
        if not cache_key:
            cache_key = self.get_cache_key()

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

    
    def get_presist_compliation(self):
        with open("user_data/compliations.json", "r") as file:
            return json.load(file)

    #
    
    def set_user_extract_cv_data(self, user_cv_data, pdf_path):
        with open("user_data/user_extracted_cv.json", "w") as file:
            _pdf_path = self.get_upload_file_name(pdf_path)
            return json.dump({"data": user_cv_data, "filename": _pdf_path}, file)

    
    def unset_user_extract_cv_data(self):
        os.remove("user_data/user_extracted_cv.json")

    
    def has_user_extract_cv_data(self):
        return os.path.exists("user_data/user_extracted_cv.json")

    
    def get_user_extract_cv_data(self):
        with open("user_data/user_extracted_cv.json", "r") as file:
            return json.load(file)["data"]

    
    def get_user_extract_cv_file_name(self):
        with open("user_data/user_extracted_cv.json", "r") as file:
            return json.load(file)["filename"]

    #
    
    def set_issues_to_overcome(self, issues_found):
        with open("user_data/issues_to_overcome.json", "w") as file:
            json.dump(issues_found, file)

    
    def has_issues_to_overcome(self):
        return os.path.exists("user_data/issues_to_overcome.json")

    
    def get_issues_to_overcome(self):
        with open("user_data/issues_to_overcome.json", "r") as file:
            return json.load(file)

    
    def set_chain_messages(self, id, chat_about_extracted_cv, closed=False, **kwarg):
        with open(f"user_data/chain_message_on_{id}.json", "w") as file:
            json.dump({"data": chat_about_extracted_cv, "closed": closed}, file)

    
    def has_chain_messages(self, id, closed=False, **kwrg):
        if not os.path.exists(f"user_data/chain_message_on_{id}.json"):
            return False

        with open(f"user_data/chain_message_on_{id}.json", "r") as file:
            return json.load(file)["closed"] == closed

    
    def get_chain_messages(self, id, closed=True):
        if self.has_chain_messages(id, closed=closed):
            with open(f"user_data/chain_message_on_{id}.json", "r") as file:
                return json.load(file)["data"]
        else:
            return []

    
    def set_completed_cv_data(self, user_cv_data):
        if os.path.exists("user_data/user_completed_cv.json"):
            with open("user_data/user_completed_cv.json", "r") as file:
                complete = json.load(file)
        else:
            complete = {}
        complete[self.get_datetime_str()] = user_cv_data
        with open("user_data/user_completed_cv.json", "w") as file:
            return json.dump(complete, file)

    
    def has_completed_cv_data(self):
        return os.path.exists("user_data/user_completed_cv.json")

    
    def get_completed_cv_data(self):
        with open("user_data/user_completed_cv.json", "r") as file:
            complete = json.load(file)
            return complete[max(complete.keys(), key=lambda x: self.str_to_datetime(x))]

    #

    
    def set_drill_down_communiation(self, drill_down):
        with open("user_data/user_drill_down.json", "w") as file:
            return json.dump(drill_down, file)

    #
    
    def set_position_data(self, position_name, user_position_data):
        if not os.path.exists("user_data/user_position.json"):
            exiting = {}
        else:
            with open("user_data/user_position.json", "r") as file:
                exiting = json.load(file)
        exiting[position_name] = user_position_data
        with open("user_data/user_position.json", "w") as file:
            json.dump(exiting, file)

    
    def has_position_data(self, position_name=None):
        if not os.path.exists("user_data/user_position.json"):
            return False
        elif position_name:
            return self.get_position_data(position_name) != None
        else:
            return True

    
    def get_position_data(self, position_name=None):
        with open("user_data/user_position.json", "r") as file:
            response = json.load(file)

            if position_name:
                return response.get(position_name, None)
            return response

    #
    
    def set_position_cv_offers(self, list_of_cvs_options, current_conversation):
        existing = {}
        if os.path.exists("user_data/user_position_cv_offers.json"):
            with open(f"user_data/user_position_cv_offers.json", "r") as file:
                existing = json.load(file)

        existing[current_conversation] = (
            list_of_cvs_options
            if isinstance(list_of_cvs_options, list)
            else [list_of_cvs_options]
        )
        with open(f"user_data/user_position_cv_offers.json", "w") as file:
            json.dump(existing, file)

    
    def has_position_cv_offers(self, current_conversation):
        if not os.path.exists("user_data/user_position_cv_offers.json"):
            return False
        with open(f"user_data/user_position_cv_offers.json", "r") as file:
            return current_conversation in json.load(file)

    
    def get_all_position_cv_offers(self, current_conversation):
        with open(f"user_data/user_position_cv_offers.json", "r") as file:
            return list(map(lambda x: x["cv"], json.load(file)[current_conversation]))

    
    def get_all_position_cv_cover_letters(self, current_conversation):
        with open(f"user_data/user_position_cv_offers.json", "r") as file:
            return list(
                map(lambda x: x["message"], json.load(file)[current_conversation])
            )

    #
    
    def set_identified_gap_from_hiring_team(self, gaps_to_adresss):
        with open(f"user_data/identified_gap_from_hiring_team.json", "w") as file:
            json.dump(gaps_to_adresss, file)

    
    def has_identified_gap_from_hiring_team(self):
        return os.path.exists("user_data/identified_gap_from_hiring_team.json")

    
    def get_identified_gap_from_hiring_team(self):
        with open(f"user_data/identified_gap_from_hiring_team.json", "r") as file:
            return json.load(file)

    #

    
    def set_base_optimized(self, user_cv, gen_id):
        if os.path.exists("user_data/base_optimized.json"):
            with open(f"user_data/base_optimized.json", "r") as file:
                content = json.load(file)
        else:
            content = {}

        content[gen_id] = user_cv
        with open(f"user_data/base_optimized.json", "w") as file:
            json.dump(content, file)

    
    def has_optimized_cv(self, gen_id):
        if not os.path.exists("user_data/base_optimized.json"):
            return False
        with open(f"user_data/base_optimized.json", "r") as file:
            return gen_id in json.load(file)

    
    def get_base_optimized(self, gen_id):
        with open(f"user_data/base_optimized.json", "r") as file:
            return json.load(file)[gen_id]

    
    def set_issues_to_solve_in_chat(self, issues_to_solve, gen_id):
        if os.path.exists("user_data/issues_to_solve_in_chat.json"):
            with open(f"user_data/issues_to_solve_in_chat.json", "r") as file:
                content = json.load(file)
        else:
            content = {}

        content[gen_id] = issues_to_solve
        with open(f"user_data/issues_to_solve_in_chat.json", "w") as file:
            json.dump(content, file)

    
    def get_issues_to_solve_in_chat(self, gen_id):
        with open(f"user_data/issues_to_solve_in_chat.json", "r") as file:
            return json.load(file)[gen_id]

    #
    
    def set_pdfs_files(self, pdf, current_conversation):
        existing = {}
        if os.path.exists("user_data/pdf_paths.json"):
            with open(f"user_data/pdf_paths.json", "r") as file:
                existing = json.load(file)
        existing[current_conversation] = pdf

        with open(f"user_data/pdf_paths.json", "w") as file:
            return json.dump(existing, file)

    
    def has_pdfs_files(self, current_conversation):
        if not os.path.exists("user_data/pdf_paths.json"):
            return False

        with open(f"user_data/pdf_paths.json", "r") as file:
            return current_conversation in json.load(file)

    
    def get_pdfs_files(self, current_conversation):
        with open(f"user_data/pdf_paths.json", "r") as file:
            return json.load(file)[current_conversation]

    #

    
    def wrap_up(self, complete_path, messages):
        complete_data = {
            "message": messages,
            "extracted_cv": self.get_user_extract_cv_data(),
            "completed_cv": self.get_completed_cv_data(),
            "position_data": self.get_position_data(),
            "offers": self.get_all_position_cv_offers(),
            "all_compliation": self.get_presist_compliation(),
        }
        with open(complete_path, "w") as file:
            json.dump(complete_data, file)

        shutil.rmtree("user_data")
        os.mkdir("user_data")
