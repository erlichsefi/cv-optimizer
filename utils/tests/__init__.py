from unittest.mock import Mock
from utils.interface import TerminalInterface
import inspect


class MockUserInterface(TerminalInterface):
     def __init__(self):
        #super().__init__()
        # Dynamically mock all methods of TerminalInterface
        for name, method in inspect.getmembers(TerminalInterface, predicate=inspect.isfunction):
            setattr(self, name, Mock(name=name))