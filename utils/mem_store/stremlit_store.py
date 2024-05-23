import json
import os
import shutil

import streamlit as st
from .base_store import StateStore


class StermlitStateStore(StateStore):

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
    def set_user_extract_cv_data(cls, user_cv_data,file_name):
        st.session_state["user_extracted_cv"] = user_cv_data
        st.session_state["file_name_uploaded"] = file_name.name

    @classmethod
    def unset_user_extract_cv_data(cls):
        st.session_state.pop("user_extracted_cv")
        st.session_state.pop("file_name_uploaded")

    @classmethod
    def get_user_extract_cv_file_name(cls):
        return st.session_state["file_name_uploaded"]

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
    def set_chain_messages(cls, id, chat_about_extracted_cv, closed=False, **kwarg):
        st.session_state[f"chain_message_on_{id}"] = {
            "data": chat_about_extracted_cv,
            "closed": closed,
        }

    @classmethod
    def has_chain_messages(cls, id, closed=False, **kwrg):
        return (
            f"chain_message_on_{id}" in st.session_state
            and st.session_state[f"chain_message_on_{id}"]["closed"] == closed
        )

    @classmethod
    def get_chain_messages(cls, id):
        if cls.has_chain_messages(id):
            return st.session_state[f"chain_message_on_{id}"]["data"]
        return []

    #
    @classmethod
    def set_completed_cv_data(cls, user_cv_data):
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
        return complete[max(complete.keys(), key=lambda x: cls.str_to_datetime(x))]

    #
    @classmethod
    def set_drill_down_communiation(cls, drill_down):
        st.session_state["user_drill_down"] = drill_down

    #
    @classmethod
    def set_position_data(cls,position_name, user_position_data):

        if "user_position" not in st.session_state:
            exiting = {}
        else:
            exiting = st.session_state['user_position']

        exiting[position_name]= user_position_data
        st.session_state['user_position'] = exiting
            

    @classmethod
    def has_position_data(cls,position_name=None):
        return "user_position" in st.session_state and (not position_name or position_name in st.session_state['user_position'])

    @classmethod
    def get_position_data(cls,position_name):
        return st.session_state["user_position"][position_name]

    #
    @classmethod
    def set_position_cv_offers(cls, list_of_cvs_options):
        st.session_state["user_position_cv_offers"] = list_of_cvs_options

    @classmethod
    def has_position_cv_offers(cls):
        return "user_position_cv_offers" in st.session_state

    @classmethod
    def get_all_position_cv_offers(cls):
        return st.session_state["user_position_cv_offers"]
    

    @classmethod
    def set_identified_gap_from_hiring_team(cls, gaps_to_adresss):
        st.session_state['identified_gap_from_hiring_team'] = gaps_to_adresss


    @classmethod
    def has_identified_gap_from_hiring_team(cls):
        return "identified_gap_from_hiring_team" in st.session_state

    @classmethod
    def get_identified_gap_from_hiring_team(cls):
        return st.session_state['identified_gap_from_hiring_team']
    #

    @classmethod
    def set_base_optimized(cls, user_cv, gen_id):
        if "base_optimized" in st.session_state:
            content = st.session_state['base_optimized']
        else:
            content = {}

        content[gen_id] = user_cv
        st.session_state['base_optimized'] = content

    @classmethod
    def has_optimized_cv(cls, gen_id):
        if "base_optimized" not in st.session_state:
            return False
        return gen_id in st.session_state['base_optimized']

    @classmethod
    def get_base_optimized(cls, gen_id):
        return st.session_state['base_optimized'][gen_id]

    @classmethod
    def set_issues_to_solve_in_chat(cls, issues_to_solve, gen_id):
        if "issues_to_solve_in_chat" in st.session_state:
            content = st.session_state['base_optimized']
        else:
            content = {}

        content[gen_id] = issues_to_solve
        st.session_state['issues_to_solve_in_chat'] = content

    @classmethod
    def get_issues_to_solve_in_chat(cls, gen_id):
        return st.session_state['issues_to_solve_in_chat'][gen_id]

