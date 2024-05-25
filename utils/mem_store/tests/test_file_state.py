from utils.mem_store.file_store import FileStateStore
from test_cases import make_test_case
import json
import os
import tempfile

class FileSetup():


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

class FileStateStoreTestCase(make_test_case(FileStateStore,FileSetup())):
    pass



