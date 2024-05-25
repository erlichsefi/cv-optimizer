import unittest
import json
import os
import tempfile
from utils.mem_store.file_store import FileStateStore

class TestFileStateStore(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir.name)
        
        # Create required directories and files
        os.makedirs("blueprints", exist_ok=True)
        os.makedirs("user_data", exist_ok=True)
        
        with open("blueprints/cv.json", "w") as file:
            json.dump({"cv": "blueprint"}, file)
            
        with open("blueprints/position.json", "w") as file:
            json.dump({"position": "blueprint"}, file)
        
        with open("blueprints/cv.tex", "w") as file:
            file.write("latex format")

    def tearDown(self):
        # Change back to the original working directory and clean up
        os.chdir(self.original_cwd)
        self.test_dir.cleanup()

    def test_get_cv_blueprint(self):
        blueprint = FileStateStore.get_cv_blueprint()
        self.assertEqual(blueprint, {"cv": "blueprint"})
    
    def test_get_position_blueprint(self):
        blueprint = FileStateStore.get_position_blueprint()
        self.assertEqual(blueprint, {"position": "blueprint"})

    def test_get_expected_latex_format(self):
        latex_format = FileStateStore.get_expected_latex_format()
        self.assertEqual(latex_format, "latex format")

    def test_presist_compliation_and_get_presist_compliation(self):
        messages = ["message1", "message2"]
        generations = ["gen1", "gen2"]
        model = "test_model"
        cache_key = "test_cache_key"
        
        FileStateStore.presist_compliation(messages, generations, model, cache_key)
        compliations = FileStateStore.get_presist_compliation()
        expected_data = {
            "messages": messages,
            "generations": generations,
            "model": model
        }
        
        self.assertIn(cache_key, compliations)
        self.assertEqual(compliations[cache_key], expected_data)
    
    def test_set_and_get_user_extract_cv_data(self):
        user_cv_data = {"name": "test"}
        pdf_path = "test.pdf"
        
        FileStateStore.set_user_extract_cv_data(user_cv_data, pdf_path)
        self.assertTrue(FileStateStore.has_user_extract_cv_data())
        
        extracted_data = FileStateStore.get_user_extract_cv_data()
        filename = FileStateStore.get_user_extract_cv_file_name()
        
        self.assertEqual(extracted_data, user_cv_data)
        self.assertEqual(filename, pdf_path)
        
        FileStateStore.unset_user_extract_cv_data()
        self.assertFalse(FileStateStore.has_user_extract_cv_data())
    
    def test_set_and_get_issues_to_overcome(self):
        issues = ["issue1", "issue2"]
        
        FileStateStore.set_issues_to_overcome(issues)
        self.assertTrue(FileStateStore.has_issues_to_overcome())
        
        stored_issues = FileStateStore.get_issues_to_overcome()
        self.assertEqual(stored_issues, issues)
    
    def test_set_and_get_chain_messages(self):
        id = "123"
        messages = ["message1", "message2"]
        
        FileStateStore.set_chain_messages(id, messages, closed=True)
        self.assertTrue(FileStateStore.has_chain_messages(id, closed=True))
        
        chain_messages = FileStateStore.get_chain_messages(id)
        self.assertEqual(chain_messages, messages)
    
    def test_set_and_get_completed_cv_data(self):
        user_cv_data = {"cv": "data"}
        
        FileStateStore.set_completed_cv_data(user_cv_data)
        self.assertTrue(FileStateStore.has_completed_cv_data())
        
        completed_data = FileStateStore.get_completed_cv_data()
        self.assertEqual(completed_data, user_cv_data)
    
    def test_set_and_get_position_data(self):
        position_name = "position1"
        position_data = {"data": "value"}
        
        FileStateStore.set_position_data(position_name, position_data)
        self.assertTrue(FileStateStore.has_position_data(position_name))
        
        retrieved_data = FileStateStore.get_position_data(position_name)
        self.assertEqual(retrieved_data, position_data)
    
    def test_set_and_get_position_cv_offers(self):
        conversation_id = "conversation1"
        cvs_options = [{"cv": "option1", "message": "message1"}]
        
        FileStateStore.set_position_cv_offers(cvs_options, conversation_id)
        self.assertTrue(FileStateStore.has_position_cv_offers(conversation_id))
        
        cvs = FileStateStore.get_all_position_cv_offers(conversation_id)
        messages = FileStateStore.get_all_position_cv_cover_letters(conversation_id)
        
        self.assertEqual(cvs, ["option1"])
        self.assertEqual(messages, ["message1"])

    def test_set_and_get_identified_gap_from_hiring_team(self):
        gaps = ["gap1", "gap2"]
        
        FileStateStore.set_identified_gap_from_hiring_team(gaps)
        self.assertTrue(FileStateStore.has_identified_gap_from_hiring_team())
        
        retrieved_gaps = FileStateStore.get_identified_gap_from_hiring_team()
        self.assertEqual(retrieved_gaps, gaps)

    def test_set_and_get_base_optimized(self):
        gen_id = "gen1"
        user_cv = {"cv": "optimized"}
        
        FileStateStore.set_base_optimized(user_cv, gen_id)
        self.assertTrue(FileStateStore.has_optimized_cv(gen_id))
        
        optimized_cv = FileStateStore.get_base_optimized(gen_id)
        self.assertEqual(optimized_cv, user_cv)
    
    def test_set_and_get_issues_to_solve_in_chat(self):
        gen_id = "gen1"
        issues = ["issue1", "issue2"]
        
        FileStateStore.set_issues_to_solve_in_chat(issues, gen_id)
        retrieved_issues = FileStateStore.get_issues_to_solve_in_chat(gen_id)
        
        self.assertEqual(retrieved_issues, issues)
    
    def test_set_and_get_pdfs_files(self):
        conversation_id = "conversation1"
        pdf = "test.pdf"
        
        FileStateStore.set_pdfs_files(pdf, conversation_id)
        self.assertTrue(FileStateStore.has_pdfs_files(conversation_id))
        
        retrieved_pdf = FileStateStore.get_pdfs_files(conversation_id)
        self.assertEqual(retrieved_pdf, pdf)
