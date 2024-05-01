from utils.interface import TerminalInterface
from utils.extract_cv_data import run as pdf_to_user_data
from utils.complete_missing_data import run as verify_user_data
from utils.extract_position_data import run as position_snippet_to_position_data
from utils.position_cv_variations import chat_loop as overcome_gaps
from utils.dump_json_to_latex import run as to_pdfs