from deepeval import evaluate
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase
from utils.complete_missing_data import get_issues_need_to_be_adressed
import json
import random
from utils.tests import MockUserInterface


def get_perfect_cv():
    with open("data_set/expected_cv.json","r") as file:
        return json.load(file)


    
def recursive_set(json_obj,value):
    if isinstance(json_obj, dict):
        if not json_obj:
            return
        key = random.choice(list(json_obj.keys()))
        if isinstance(json_obj[key], (dict, list)):
            recursive_set(json_obj[key],value)
        else:
            json_obj[key] = value
    elif isinstance(json_obj, list):
        if not json_obj:
            return
        index = random.randint(0, len(json_obj) - 1)
        if isinstance(json_obj[index], (dict, list)):
            recursive_set(json_obj[index],value)
        else:
            json_obj[index] = value

def test_perfect_cv():
    mock = MockUserInterface()
    mock.get_user_extract_cv_data.return_value = get_perfect_cv()
    
    get_issues_need_to_be_adressed(mock)

    assert mock.set_issues_to_overcome.call_count == 1

    extracted_json = mock.set_issues_to_overcome.call_args_list[0][0][0]
    assert len(extracted_json['confirmed_question']) <= 1, json.dumps(extracted_json)


def test_perfect_cv_missing():
    prefect_cv = get_perfect_cv()
    number_of_mimes = int(random.random()*10)

    recursive_set(prefect_cv,"asdasd")
    # for _ in range(number_of_mimes):
    #     for section in prefect_cv:x
        

    mock = MockUserInterface()
    mock.get_user_extract_cv_data.return_value = prefect_cv
    
    get_issues_need_to_be_adressed(mock)

    assert mock.set_issues_to_overcome.call_count == 1

    extracted_json = mock.set_issues_to_overcome.call_args_list[0][0][0]
    assert len(extracted_json['confirmed_question']) <= 1, json.dumps(extracted_json)