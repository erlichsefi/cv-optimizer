from abc import ABC, abstractmethod
from uuid import uuid4
import json
import streamlit as st
from .llm_store import get_chat_compliation
from .mem_store import StateStore, FileStateStore, StermlitStateStore
import contextlib



class UserInterface(StateStore, ABC):

    def __init__(self) -> None:
        super().__init__()
        self.messages_history = list()

    @abstractmethod
    def get_pdf_file_from_user(self):
        pass

    @abstractmethod
    def send_user_message(self, message):
        pass

    @abstractmethod
    @contextlib.contextmanager
    def processing(self,message):
        pass

    @abstractmethod
    def get_user_input(self,messages=None):
        pass

    @abstractmethod
    def get_position_snippet_data(self):
        pass

    @abstractmethod
    def on_cv_file_received(self):
        self.send_user_message("We see the file, We are on it!")

    @abstractmethod
    def send_files(self, file_paths):
        pass

    @abstractmethod
    def start_bot_session(self, topic):
        pass

    @abstractmethod
    def end_bot_session(self):
        pass

    def wrap_up(self, uuid):
        if not uuid:
            uuid = str(uuid4())
        self.wrap_up(f"data_set/predicted/{uuid}.json", messages=self.messages_history)


class TerminalInterface(UserInterface, FileStateStore):

    def __init__(self) -> None:
        super(TerminalInterface, self).__init__()

    def send_user_message(self, message):
        self.messages_history.append({"role": "assistant", "content": message})
        print(f"Bot: {message}")

    def get_user_input(self,messages=None):
        if len(messages) == 1:
            self.send_user_message(messages[0])
        message = input("User: ")
        self.messages_history.append({"role": "user", "content": message})
        return message

    @contextlib.contextmanager
    def processing(self,message):
        self.send_user_message(message)
        yield

    def get_pdf_file_from_user(self):
        message = input("CV path: ")
        self.messages_history.append({"role": "user", "file": message})
        return message

    def on_cv_file_received(self):
        self.send_user_message("Thanks!")

    def get_position_snippet_data(self):
        self.send_user_message(
            "Enter/Paste your content. Ctrl-D or Ctrl-Z (windows) to save it."
        )
        contents = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            contents.append(line)
        full_content = "\n".join(contents)
        self.messages_history.append({"role": "user", "content": full_content})
        return full_content

    def send_files(self, file_paths):
        self.send_user_message("\n".join(file_paths))

    def start_bot_session(self, topic):
        self.send_user_message("--------------------------------------------------")
        self.send_user_message("Start chatting with the bot (type 'quit' to stop)!")
        self.send_user_message("--------------------------------------------------")
        self.send_user_message(f"Let's focus on {topic}")

    def end_bot_session(self):
        pass


class Args(TerminalInterface):

    def __init__(self, pdf_path=None) -> None:
        super().__init__()
        self.pdf_path = pdf_path

    def get_pdf_file_from_user(self):
        return self.pdf_path


class LLMTesting(TerminalInterface, FileStateStore):

    def __init__(self, how_to_act, cv_file, poistion_file, profile_file) -> None:
        super(LLMTesting, self).__init__()
        self.cv_file = cv_file
        self.poistion_file = poistion_file
        self.profile_file = profile_file
        self.current_message = ""
        self.how_to_act = how_to_act
        self._start_session()

    def _start_session(self):
        self.llm_testing_messages = []

        guideline = "- " + "\n -".join(self.how_to_act)
        with open(self.profile_file, "r") as file:
            profile_file_content = json.load(file)

        with open(self.poistion_file, "r") as file:
            poistion_text = file.readline()

        self.llm_testing_messages.append(
            {
                "role": "system",
                "content": f"""
        You are acting on behalf of a user:
        {json.dumps(profile_file_content)}
                                                      
        The user is interseted in the following position:
        {poistion_text}

        You are testing an LLM base application, answer in a short a concise manner.
        
        Follow those guidelines:
        {guideline}
        - You must answer the user question like your are a humen being.

        """,
            }
        )

    def get_pdf_file_from_user(self):
        return self.cv_file

    def get_position_snippet_data(self):
        with open(self.poistion_file, "r") as file:
            return file.readline()

    def send_user_message(self, message):
        print(f"Bot:{message}")
        self.current_message += f"\n {message}"

    def get_user_input(self,messages=None):
        self.llm_testing_messages.append({"role": "user", "content": self.current_message})

        response = get_chat_compliation(messages=self.llm_testing_messages)

        self.llm_testing_messages.append({"role": "assistant", "content": response})

        self.current_message = ""
        print(f"User Agent:{response}")
        return response


class SteamlitInterface(UserInterface, StermlitStateStore):

    def __init__(self) -> None:
        super(SteamlitInterface, self).__init__()

    def send_user_message(self, message):
        # if self.messages_history:
        with st.chat_message("assistant"):
            st.markdown(message)
        #
        self.messages_history.append({"role": "assistant", "content": message})

    @contextlib.contextmanager
    def processing(self,message):
        with st.spinner(message):
            yield      

    def get_user_input(self,messages=None):
        # print all the messages before
        if messages:
            for _, msg_dict in enumerate(messages):
                with st.chat_message(msg_dict["role"]):
                    st.markdown(msg_dict["content"])

        # ask for input
        if message := st.chat_input("User:"):

            self.messages_history.append({"role": "user", "content": message})

            with st.chat_message("user"):
                st.markdown(message)

            return message
        return None

    def get_pdf_file_from_user(self):
        return st.file_uploader(
            "Choose a file", type=["pdf"], accept_multiple_files=False
        )

    def on_cv_file_received(self):
        pass

    def get_position_snippet_data(self):
        contents = st.text_input(label="Position")
        if st.button("Go"):
            full_content = "\n".join(contents)
            self.messages_history.append({"role": "user", "content": full_content})
            return full_content

    def send_files(self, file_paths):
        self.send_user_message("\n".join(file_paths))


    def start_bot_session(self, topic):
        pass

    def end_bot_session(self):
        pass
