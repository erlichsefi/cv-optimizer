import json
import os
import shutil

import streamlit as st
from .base_store import StateStore


class StermlitStateStore(StateStore):

    
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
    
    def set_user_extract_cv_data(self, user_cv_data, file_name):
        st.session_state["user_extracted_cv"] = user_cv_data
        st.session_state["file_name_uploaded"] = self.get_upload_file_name(file_name)

    
    def unset_user_extract_cv_data(self):
        st.session_state.pop("user_extracted_cv")
        st.session_state.pop("file_name_uploaded")

    
    def get_user_extract_cv_file_name(self):
        return st.session_state["file_name_uploaded"]

    
    def has_user_extract_cv_data(self):
        return "user_extracted_cv" in st.session_state

    
    def get_user_extract_cv_data(self):
        if self.has_user_extract_cv_data():
            return st.session_state["user_extracted_cv"]

    #

    
    def set_issues_to_overcome(self, issues_found):
        st.session_state["issues_to_overcome"] = issues_found

    
    def has_issues_to_overcome(self):
        return "issues_to_overcome" in st.session_state

    
    def get_issues_to_overcome(self):
        if self.has_issues_to_overcome():
            return st.session_state["issues_to_overcome"]

    
    def set_chain_messages(self, id, chat_about_extracted_cv, closed=False, **kwarg):
        st.session_state[f"chain_message_on_{id}"] = {
            "data": chat_about_extracted_cv,
            "closed": closed,
        }

    
    def has_chain_messages(self, id, closed=False, **kwrg):
        return (
            f"chain_message_on_{id}" in st.session_state
            and st.session_state[f"chain_message_on_{id}"]["closed"] == closed
        )

    
    def get_chain_messages(self, id, closed=True):
        if self.has_chain_messages(id, closed=closed):
            return st.session_state[f"chain_message_on_{id}"]["data"]
        return []

    #
    
    def set_completed_cv_data(self, user_cv_data):
        if "user_completed_cv" in st.session_state:
            complete = st.session_state["user_completed_cv"]
        else:
            complete = {}
        complete[self.get_datetime_str()] = user_cv_data
        st.session_state["user_completed_cv"] = complete

    
    def has_completed_cv_data(self):
        return "user_completed_cv" in st.session_state

    
    def get_completed_cv_data(self):
        complete = st.session_state["user_completed_cv"]
        return complete[max(complete.keys(), key=lambda x: self.str_to_datetime(x))]

    #
    
    def set_drill_down_communiation(self, drill_down):
        st.session_state["user_drill_down"] = drill_down

    #
    
    def set_position_data(self, position_name, user_position_data):

        if "user_position" not in st.session_state:
            exiting = {}
        else:
            exiting = st.session_state["user_position"]

        exiting[position_name] = user_position_data
        st.session_state["user_position"] = exiting

    
    def has_position_data(self, position_name=None):
        return "user_position" in st.session_state and (
            not position_name or position_name in st.session_state["user_position"]
        )

    
    def get_position_data(self, position_name=None):
        response = st.session_state["user_position"]

        if position_name:
            return response[position_name]
        return response

    #
    
    def set_position_cv_offers(self, list_of_cvs_options, current_conversation):
        existing = {}
        if "user_position_cv_offers" in st.session_state:
            existing = st.session_state["user_position_cv_offers"]

        existing[current_conversation] = (
            list_of_cvs_options
            if isinstance(list_of_cvs_options, list)
            else [list_of_cvs_options]
        )
        st.session_state["user_position_cv_offers"] = existing

    
    def has_position_cv_offers(self, current_conversation):
        return (
            "user_position_cv_offers" in st.session_state
            and current_conversation in st.session_state["user_position_cv_offers"]
        )

    
    def get_all_position_cv_offers(self, current_conversation):
        return list(
            map(
                lambda x: x["cv"],
                st.session_state["user_position_cv_offers"][current_conversation],
            )
        )

    
    def get_all_position_cv_cover_letters(self, current_conversation):
        return list(
            map(
                lambda x: x["message"],
                st.session_state["user_position_cv_offers"][current_conversation],
            )
        )

    
    def set_identified_gap_from_hiring_team(self, gaps_to_adresss):
        st.session_state["identified_gap_from_hiring_team"] = gaps_to_adresss

    
    def has_identified_gap_from_hiring_team(self):
        return "identified_gap_from_hiring_team" in st.session_state

    
    def get_identified_gap_from_hiring_team(self):
        return st.session_state["identified_gap_from_hiring_team"]

    #

    
    def set_base_optimized(self, user_cv, gen_id):
        if "base_optimized" in st.session_state:
            content = st.session_state["base_optimized"]
        else:
            content = {}

        content[gen_id] = user_cv
        st.session_state["base_optimized"] = content

    
    def has_optimized_cv(self, gen_id):
        if "base_optimized" not in st.session_state:
            return False
        return gen_id in st.session_state["base_optimized"]

    
    def get_base_optimized(self, gen_id):
        return st.session_state["base_optimized"][gen_id]

    
    def set_issues_to_solve_in_chat(self, issues_to_solve, gen_id):
        if "issues_to_solve_in_chat" in st.session_state:
            content = st.session_state["base_optimized"]
        else:
            content = {}

        content[gen_id] = issues_to_solve
        st.session_state["issues_to_solve_in_chat"] = content

    
    def get_issues_to_solve_in_chat(self, gen_id):
        return st.session_state["issues_to_solve_in_chat"][gen_id]

    
    def set_pdfs_files(self, pdf, current_conversation):
        if "pdf_paths" in st.session_state:
            content = st.session_state["pdf_paths"]
        else:
            content = {}
        content[current_conversation] = pdf
        st.session_state["pdf_paths"] = content

    
    def has_pdfs_files(self, current_conversation):
        return (
            "pdf_paths" in st.session_state
            and current_conversation in st.session_state["pdf_paths"]
        )

    
    def get_pdfs_files(self, current_conversation):
        return st.session_state["pdf_paths"][current_conversation]
