
from abc import ABC,abstractmethod
from .llm_store import get_chat_compliation

class UserInterface(ABC):

    @abstractmethod
    def get_pdf_file_from_user(self):
        pass

    @abstractmethod
    def send_user_message(self,message):
        pass

    @abstractmethod
    def get_user_input(self):
        pass

    @abstractmethod
    def get_position_snippet_data(self):
        pass

    @abstractmethod
    def send_cv_files(self,file_paths):
        pass


class TerminalInterface(UserInterface):

    def send_user_message(self,message):
        print(f"Bot: {message}")

    def get_user_input(self):
        return input("User: ")
    
    def get_pdf_file_from_user(self):
        return input("CV path: ")
    
    def get_position_snippet_data(self):
        self.send_user_message("Enter/Paste your content. Ctrl-D or Ctrl-Z (windows) to save it.")
        contents = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            contents.append(line)
        return "\n".join(contents)
    
    def send_cv_files(self,file_paths):
        self.send_user_message("\n".join(file_paths))
    

class LLMTesting(UserInterface):


    def __init__(self,system_message,cv_file,poistion_text) -> None:
        super().__init__()
        self.cv_file = cv_file
        self.poistion_text = poistion_text
        self.system_message = system_message
        self.messages = list()

    def get_pdf_file_from_user(self):
        return self.cv_file
    
    def get_position_snippet_data(self):
        return self.poistion_text
    
    def send_user_message(self,message):
        self.messages.append({"role":"user","content":message})

    def get_user_input(self):
        return get_chat_compliation(messages=self.messages)
    
    def send_cv_files(self,file_paths):
        return file_paths
