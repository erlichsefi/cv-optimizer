from utils.models.cv import model_from_json
import json


def test_model_to_json():
    with open("data_set/expected_cv.json", "r") as file:
        prefect_cv = json.load(file)

    cv_model = model_from_json(prefect_cv)
    main_model_schema = cv_model.model_dump()

    main_model_schema2 = model_from_json(main_model_schema)

    assert main_model_schema2 == main_model_schema2
