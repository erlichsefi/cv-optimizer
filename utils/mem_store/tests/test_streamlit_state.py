from utils.mem_store.stremlit_store import StermlitStateStore
from test_cases import make_test_case
import json
import os
import tempfile
from unittest.mock import patch, MagicMock
import streamlit as st

class StreamlitSetup():

    mock_session_state = {"A":"a"}

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
        
        self.session_state_patch = patch('streamlit.session_state', new_callable=lambda:self.mock_session_state)
        self.mock_session_state = self.session_state_patch.start()

    def tearDown(self):
        self.session_state_patch.stop()

class FileStateStoreTestCase(make_test_case(StermlitStateStore,StreamlitSetup())):
    pass



