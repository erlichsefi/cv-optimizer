
from abc import ABC,abstractmethod

class UserInterface(ABC):

    @abstractmethod
    def send_user_message(cls,message):
        pass

    @abstractmethod
    def get_user_input(cls):
        pass

    @abstractmethod
    def get_multiliner_user_input(cls):
        pass


class TerminalInterface(UserInterface):

    def send_user_message(cls,message):
        print(f"Bot: {message}")

    def get_user_input(cls):
        return input("User: ")
    

    def get_multiliner_user_input(cls):
        cls.send_user_message("Enter/Paste your content. Ctrl-D or Ctrl-Z (windows) to save it.")
        contents = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            contents.append(line)
        return "\n".join(contents)