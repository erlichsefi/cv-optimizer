import json
import firebase_admin
from firebase_admin import credentials, firestore, storage
from datetime import datetime
from .base_store import StateStore


class FirebaseStateStore(StateStore):

    def __init__(self, user_id):
        # Check if the default app is already initialized
        if not firebase_admin._apps:
            cred = credentials.Certificate("cv-optimization-firebase-adminsdk.json")
            firebase_admin.initialize_app(cred, {
                'storageBucket': 'cv-optimization.appspot.com',
            })
        
        # Initialize Firestore and Storage with the default app
        self.db = firestore.client()
        self.bucket = storage.bucket()
        self.user_id = user_id
        self.messages_history = list()

    def _get_document(self, collection_name):
        doc_ref = self.db.collection(collection_name).document(self.user_id)
        doc = doc_ref.get()
        return doc_ref, doc

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
    def get_presist_compliation(cls):   
        doc_ref = cls.db.collection("user_data").document("compliations")
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            raise FileNotFoundError("Position Blueprint not found in Firestore")
        
    @classmethod
    def set_drill_down_communiation(cls):   
        doc_ref = cls.db.collection("user_data").document("user_drill_down")
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            raise FileNotFoundError("Position Blueprint not found in Firestore")
        
    @classmethod
    def presist_compliation(cls, messages, generations, model, cache_key=None):
        if not cache_key:
            cache_key = cls.get_cache_key()
        
        data = {
            "messages": messages,
            "generations": generations,
            "model": model,
        }
        doc_ref, _ = cls._get_document("user_data")
        existing_data = doc_ref.get().to_dict() if doc_ref.get().exists else {}
        existing_data[cache_key] = data
        doc_ref.set(existing_data, merge=True)


    def persist_compilation(self, messages, generations, model, cache_key=None):
        if not cache_key:
            cache_key = self.get_cache_key()
        
        data = {
            "messages": messages,
            "generations": generations,
            "model": model,
        }
        self.db.collection("user_data").document(cache_key).set(data)

    def get_persist_compilation(self, cache_key):
        doc_ref, doc = self._get_document("user_data")
        if doc.exists:
            return doc.to_dict()
        else:
            raise FileNotFoundError(f"Compilation with cache_key {cache_key} not found in Firestore")

    def set_user_extract_cv_data(self, user_cv_data, file_name):
        data = {
            "user_extracted_cv": user_cv_data,
            "file_name_uploaded": self.get_upload_file_name(file_name)
        }
        doc_ref, _ = self._get_document("user_sessions")
        doc_ref.set(data, merge=True)

    def unset_user_extract_cv_data(self):
        doc_ref, _ = self._get_document("user_sessions")
        doc_ref.update({
            "user_extracted_cv": firestore.DELETE_FIELD,
            "file_name_uploaded": firestore.DELETE_FIELD
        })

    def get_user_extract_cv_file_name(self):
        _, doc = self._get_document("user_sessions")
        if doc.exists and "file_name_uploaded" in doc.to_dict():
            return doc.to_dict()["file_name_uploaded"]
        return None

    def has_user_extract_cv_data(self):
        _, doc = self._get_document("user_sessions")
        return doc.exists and "user_extracted_cv" in doc.to_dict()

    def get_user_extract_cv_data(self):
        if self.has_user_extract_cv_data():
            _, doc = self._get_document("user_sessions")
            return doc.to_dict().get("user_extracted_cv")
        return None

    def set_issues_to_overcome(self, issues_found):
        doc_ref, _ = self._get_document("user_sessions")
        doc_ref.set({"issues_to_overcome": issues_found}, merge=True)

    def has_issues_to_overcome(self):
        _, doc = self._get_document("user_sessions")
        return doc.exists and "issues_to_overcome" in doc.to_dict()

    def get_issues_to_overcome(self):
        if self.has_issues_to_overcome():
            _, doc = self._get_document("user_sessions")
            return doc.to_dict().get("issues_to_overcome")
        return None

    def set_chain_messages(self, chain_id, chat_about_extracted_cv, closed=False):
        data = {
            f"chain_message_on_{chain_id}": {
                "data": chat_about_extracted_cv,
                "closed": closed,
            }
        }
        doc_ref, _ = self._get_document("user_sessions")
        doc_ref.set(data, merge=True)

    def has_chain_messages(self, chain_id, closed=False):
        _, doc = self._get_document("user_sessions")
        chain_key = f"chain_message_on_{chain_id}"
        return doc.exists and chain_key in doc.to_dict() and doc.to_dict()[chain_key]["closed"] == closed

    def get_chain_messages(self, chain_id, closed=True):
        if self.has_chain_messages(chain_id, closed=closed):
            _, doc = self._get_document("user_sessions")
            return doc.to_dict()[f"chain_message_on_{chain_id}"]["data"]
        return []

    def set_completed_cv_data(self, user_cv_data):
        doc_ref, doc = self._get_document("user_sessions")
        complete = doc.to_dict().get("user_completed_cv", {}) if doc.exists else {}
        complete[self.get_datetime_str()] = user_cv_data
        doc_ref.set({"user_completed_cv": complete}, merge=True)

    def has_completed_cv_data(self):
        _, doc = self._get_document("user_sessions")
        return doc.exists and "user_completed_cv" in doc.to_dict()

    def get_completed_cv_data(self):
        if self.has_completed_cv_data():
            _, doc = self._get_document("user_sessions")
            complete = doc.to_dict()["user_completed_cv"]
            return complete[max(complete.keys(), key=lambda x: self.str_to_datetime(x))]
        return None

    def set_drill_down_communication(self, drill_down):
        doc_ref, _ = self._get_document("user_sessions")
        doc_ref.set({"user_drill_down": drill_down}, merge=True)

    def set_position_data(self, position_name, user_position_data):
        doc_ref, doc = self._get_document("user_sessions")
        existing = doc.to_dict().get("user_position", {}) if doc.exists else {}
        existing[position_name] = user_position_data
        doc_ref.set({"user_position": existing}, merge=True)

    def has_position_data(self, position_name=None):
        _, doc = self._get_document("user_sessions")
        if position_name:
            return doc.exists and "user_position" in doc.to_dict() and position_name in doc.to_dict()["user_position"]
        return doc.exists and "user_position" in doc.to_dict()

    def get_position_data(self, position_name=None):
        _, doc = self._get_document("user_sessions")
        if doc.exists and "user_position" in doc.to_dict():
            response = doc.to_dict()["user_position"]
            if position_name:
                return response.get(position_name)
            return response
        return None

    def set_position_cv_offers(self, list_of_cvs_options, current_conversation):
        doc_ref, doc = self._get_document("user_sessions")
        existing = doc.to_dict().get("user_position_cv_offers", {}) if doc.exists else {}
        existing[current_conversation] = list_of_cvs_options if isinstance(list_of_cvs_options, list) else [list_of_cvs_options]
        doc_ref.set({"user_position_cv_offers": existing}, merge=True)

    def has_position_cv_offers(self, current_conversation):
        _, doc = self._get_document("user_sessions")
        return doc.exists and "user_position_cv_offers" in doc.to_dict() and current_conversation in doc.to_dict()["user_position_cv_offers"]

    def get_all_position_cv_offers(self, current_conversation):
        _, doc = self._get_document("user_sessions")
        if doc.exists and "user_position_cv_offers" in doc.to_dict():
            return list(map(lambda x: x["cv"], doc.to_dict()["user_position_cv_offers"][current_conversation]))
        return []

    def get_all_position_cv_cover_letters(self, current_conversation):
        _, doc = self._get_document("user_sessions")
        if doc.exists and "user_position_cv_offers" in doc.to_dict():
            return list(map(lambda x: x["message"], doc.to_dict()["user_position_cv_offers"][current_conversation]))
        return []

    def set_identified_gap_from_hiring_team(self, gaps_to_address):
        doc_ref, _ = self._get_document("user_sessions")
        doc_ref.set({"identified_gap_from_hiring_team": gaps_to_address}, merge=True)

    def has_identified_gap_from_hiring_team(self):
        _, doc = self._get_document("user_sessions")
        return doc.exists and "identified_gap_from_hiring_team" in doc.to_dict()

    def get_identified_gap_from_hiring_team(self):
        if self.has_identified_gap_from_hiring_team():
            _, doc = self._get_document("user_sessions")
            return doc.to_dict().get("identified_gap_from_hiring_team")
        return None

    def set_base_optimized(self, user_cv, gen_id):
        doc_ref, doc = self._get_document("user_sessions")
        content = doc.to_dict().get("base_optimized", {}) if doc.exists else {}
        content[gen_id] = user_cv
        doc_ref.set({"base_optimized": content}, merge=True)

    def has_optimized_cv(self, gen_id):
        _, doc = self._get_document("user_sessions")
        return doc.exists and "base_optimized" in doc.to_dict() and gen_id in doc.to_dict()["base_optimized"]

    def get_base_optimized(self, gen_id):
        _, doc = self._get_document("user_sessions")
        if doc.exists and "base_optimized" in doc.to_dict():
            return doc.to_dict()["base_optimized"].get(gen_id)
        return None

    def set_issues_to_solve_in_chat(self, issues_to_solve, gen_id):
        doc_ref, doc = self._get_document("user_sessions")
        content = doc.to_dict().get("issues_to_solve_in_chat", {}) if doc.exists else {}
        content[gen_id] = issues_to_solve
        doc_ref.set({"issues_to_solve_in_chat": content}, merge=True)

    def get_issues_to_solve_in_chat(self, gen_id):
        _, doc = self._get_document("user_sessions")
        if doc.exists and "issues_to_solve_in_chat" in doc.to_dict():
            return doc.to_dict()["issues_to_solve_in_chat"].get(gen_id)
        return None

    def set_pdfs_files(self, pdf, current_conversation):
        doc_ref, doc = self._get_document("user_sessions")
        content = doc.to_dict().get("pdf_paths", {}) if doc.exists else {}
        content[current_conversation] = pdf
        doc_ref.set({"pdf_paths": content}, merge=True)

    def has_pdfs_files(self, current_conversation):
        _, doc = self._get_document("user_sessions")
        return doc.exists and "pdf_paths" in doc.to_dict() and current_conversation in doc.to_dict()["pdf_paths"]

    def get_pdfs_files(self, current_conversation):
        _, doc = self._get_document("user_sessions")
        if doc.exists and "pdf_paths" in doc.to_dict():
            return doc.to_dict()["pdf_paths"].get(current_conversation)
        return None

    @staticmethod
    def get_datetime_str():
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def str_to_datetime(date_str):
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
