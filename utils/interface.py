
from abc import ABC,abstractmethod
from uuid import uuid4
import json
from .llm_store import get_chat_compliation
from .filestore import wrap_up

class UserInterface(ABC):

    def __init__(self) -> None:
        super().__init__()
        self.messages = list()

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

    
    def wrap_up(self,uuid):
        if not uuid:
            uuid = str(uuid4())
        wrap_up(f"{uuid}.json",messages=self.messages)


class TerminalInterface(UserInterface):

    def __init__(self) -> None:
        super(TerminalInterface,self).__init__()

    def send_user_message(self,message):
        self.messages.append({"role":"assistant","content":message})
        print(f"Bot: {message}")

    def get_user_input(self):
        message =  input("User: ")
        self.messages.append({"role":"user","content":message})
        return message
    
    def get_pdf_file_from_user(self):
        message = input("CV path: ")
        self.messages.append({"role":"user","file":message})
        return message
    
    def get_position_snippet_data(self):
        self.send_user_message("Enter/Paste your content. Ctrl-D or Ctrl-Z (windows) to save it.")
        contents = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            contents.append(line)
        full_content =  "\n".join(contents)
        self.messages.append({"role":"user","content":full_content})
        return full_content
    
    def send_cv_files(self,file_paths):
        self.send_user_message("\n".join(file_paths))
    

class LLMTesting(TerminalInterface):

    def __init__(self,how_to_act,cv_file,poistion_text,profile_file) -> None:
        super(LLMTesting,self).__init__()
        self.cv_file = cv_file
        self.poistion_text = poistion_text
        self.profile_file = profile_file

        guideline = '\n-'.join(how_to_act)
        with open(profile_file,"r") as file:
            profile_file_content = json.load(file)
        self.messages.append( {"role":"system","content":f"""
        You are acting on behalf of a user:
        {json.dumps(profile_file_content)}
                                                      
        interseted in the following position:
        {poistion_text}

        You are testing an LLM base application, answer in a short a concise manner.
        Follow those guidelines:

        {guideline}
        - You must answer the user question like your are a humen being.

        """})
        self.current_message = ""

    def get_pdf_file_from_user(self):
        return self.cv_file
    
    def get_position_snippet_data(self):
        return self.poistion_text
    
    def send_user_message(self,message):
        print(f"Bot:{message}")
        self.current_message += f"\n {message}"

    def get_user_input(self):
        self.messages.append({"role":"user","content":self.current_message})
        self.current_message = ""
        response = get_chat_compliation(messages=self.messages)
        print(f"User Agent:{response}")
        
        self.messages.append({"role":"assistant","content":response})
        return response
    
    def send_cv_files(self,file_paths):
        return file_paths

