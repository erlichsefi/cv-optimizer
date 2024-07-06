import json
import os
import shutil
from .base_store import StateStore


class FileStateStore(StateStore):

    def __init__(self, resources_dir):
        super().__init__(resources_dir)
        self.user_data_dir = os.path.join(resources_dir, "user_data")
        self.compliations = self._user_data_path_to("compliations.json")
        self.user_extracted_cv = self._user_data_path_to("user_extracted_cv.json")
        self.issues_to_overcome = self._user_data_path_to("issues_to_overcome.json")
        self.user_completed_cv = self._user_data_path_to("user_completed_cv.json")
        self.user_drill_down = self._user_data_path_to("user_drill_down.json")
        self.user_position = self._user_data_path_to("user_position.json")
        self.user_position_cv_offers = self._user_data_path_to(
            "user_position_cv_offers.json"
        )
        self.identified_gap_from_hiring_team = self._user_data_path_to(
            "identified_gap_from_hiring_team.json"
        )
        self.base_optimized = self._user_data_path_to("base_optimized.json")
        self.issues_to_solve_in_chat = self._user_data_path_to(
            "issues_to_solve_in_chat.json"
        )
        self.pdf_paths = self._user_data_path_to("pdf_paths.json")

    def _user_data_path_to(self, file_name):
        return os.path.join(self.user_data_dir, file_name)

    def presist_compliation(self, messages, generations, model, cache_key=None):
        if not cache_key:
            cache_key = self.get_cache_key()

        exsiting = {}

        if os.path.exists(self.compliations):
            with open(self.compliations, "r") as file:
                exsiting = json.load(file)

        exsiting[cache_key] = {
            "messages": messages,
            "generations": generations,
            "model": model,
        }

        # dump
        with open(self.compliations, "w") as file:
            json.dump(exsiting, file)

    def get_presist_compliation(self):
        with open(self.compliations, "r") as file:
            return json.load(file)

    def set_user_extract_cv_data(self, user_cv_data, pdf_path):
        with open(self.user_extracted_cv, "w") as file:
            _pdf_path = self.get_upload_file_name(pdf_path)
            return json.dump({"data": user_cv_data, "filename": _pdf_path}, file)

    def unset_user_extract_cv_data(self):
        os.remove(self.user_extracted_cv)

    def has_user_extract_cv_data(self):
        return os.path.exists(self.user_extracted_cv)

    def get_user_extract_cv_data(self):
        with open(self.user_extracted_cv, "r") as file:
            return json.load(file)["data"]

    def get_user_extract_cv_file_name(self):
        with open(self.user_extracted_cv, "r") as file:
            return json.load(file)["filename"]

    #
    def set_issues_to_overcome(self, issues_found):
        with open(self.issues_to_overcome, "w") as file:
            json.dump(issues_found, file)

    def has_issues_to_overcome(self):
        return os.path.exists(self.issues_to_overcome)

    def get_issues_to_overcome(self):
        with open(self.issues_to_overcome, "r") as file:
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
        if os.path.exists(self.user_completed_cv):
            with open(self.user_completed_cv, "r") as file:
                complete = json.load(file)
        else:
            complete = {}
        complete[self.get_datetime_str()] = user_cv_data
        with open(self.user_completed_cv, "w") as file:
            return json.dump(complete, file)

    def has_completed_cv_data(self):
        return os.path.exists(self.user_completed_cv)

    def get_completed_cv_data(self):
        with open(self.user_completed_cv, "r") as file:
            complete = json.load(file)
            return complete[max(complete.keys(), key=lambda x: self.str_to_datetime(x))]

    #
    def set_drill_down_communiation(self, drill_down):
        with open(self.user_drill_down, "w") as file:
            return json.dump(drill_down, file)

    #

    def set_position_data(self, position_name, user_position_data):
        if not os.path.exists(self.user_position):
            exiting = {}
        else:
            with open(self.user_position, "r") as file:
                exiting = json.load(file)
        exiting[position_name] = user_position_data
        with open(self.user_position, "w") as file:
            json.dump(exiting, file)

    def has_position_data(self, position_name=None):
        if not os.path.exists(self.user_position):
            return False
        elif position_name:
            return self.get_position_data(position_name) != None
        else:
            return True

    def get_position_data(self, position_name=None):
        with open(self.user_position, "r") as file:
            response = json.load(file)

            if position_name:
                return response.get(position_name, None)
            return response

    #

    def set_position_cv_offers(self, list_of_cvs_options, current_conversation):
        existing = {}
        if os.path.exists(self.user_position_cv_offers):
            with open(self.user_position_cv_offers, "r") as file:
                existing = json.load(file)

        existing[current_conversation] = (
            list_of_cvs_options
            if isinstance(list_of_cvs_options, list)
            else [list_of_cvs_options]
        )
        with open(self.user_position_cv_offers, "w") as file:
            json.dump(existing, file)

    def has_position_cv_offers(self, current_conversation):
        if not os.path.exists(self.user_position_cv_offers):
            return False
        with open(self.user_position_cv_offers, "r") as file:
            return current_conversation in json.load(file)

    def get_all_position_cv_offers(self, current_conversation):
        with open(self.user_position_cv_offers, "r") as file:
            return list(map(lambda x: x["cv"], json.load(file)[current_conversation]))

    def get_all_position_cv_cover_letters(self, current_conversation):
        with open(self.user_position_cv_offers, "r") as file:
            return list(
                map(lambda x: x["message"], json.load(file)[current_conversation])
            )

    #

    def set_identified_gap_from_hiring_team(self, gaps_to_adresss):
        with open(self.identified_gap_from_hiring_team, "w") as file:
            json.dump(gaps_to_adresss, file)

    def has_identified_gap_from_hiring_team(self):
        return os.path.exists(self.identified_gap_from_hiring_team)

    def get_identified_gap_from_hiring_team(self):
        with open(self.identified_gap_from_hiring_team, "r") as file:
            return json.load(file)

    #

    def set_base_optimized(self, user_cv, gen_id):
        if os.path.exists(self.base_optimized):
            with open(self.base_optimized, "r") as file:
                content = json.load(file)
        else:
            content = {}

        content[gen_id] = user_cv
        with open(self.base_optimized, "w") as file:
            json.dump(content, file)

    def has_optimized_cv(self, gen_id):
        if not os.path.exists(self.base_optimized):
            return False
        with open(self.base_optimized, "r") as file:
            return gen_id in json.load(file)

    def get_base_optimized(self, gen_id):
        with open(self.base_optimized, "r") as file:
            return json.load(file)[gen_id]

    def set_issues_to_solve_in_chat(self, issues_to_solve, gen_id):
        if os.path.exists(self.issues_to_solve_in_chat):
            with open(self.issues_to_solve_in_chat, "r") as file:
                content = json.load(file)
        else:
            content = {}

        content[gen_id] = issues_to_solve
        with open(self.issues_to_solve_in_chat, "w") as file:
            json.dump(content, file)

    def get_issues_to_solve_in_chat(self, gen_id):
        with open(self.issues_to_solve_in_chat, "r") as file:
            return json.load(file)[gen_id]

    #

    def set_pdfs_files(self, pdf, current_conversation):
        existing = {}
        if os.path.exists(self.pdf_paths):
            with open(self.pdf_paths, "r") as file:
                existing = json.load(file)
        existing[current_conversation] = pdf

        with open(self.pdf_paths, "w") as file:
            return json.dump(existing, file)

    def has_pdfs_files(self, current_conversation):
        if not os.path.exists(self.pdf_paths):
            return False

        with open(self.pdf_paths, "r") as file:
            return current_conversation in json.load(file)

    def get_pdfs_files(self, current_conversation):
        with open(self.pdf_paths, "r") as file:
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

        shutil.rmtree(self.user_data_dir)
        os.mkdir(self.user_data_dir)
