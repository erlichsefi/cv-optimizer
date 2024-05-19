import utils
import os
import pipeline


if __name__ == "__main__":

    poistion_folder = "data_set/positions"
    cv_file = "data_set/Curriculum_Vitae_Jan24.pdf"
    expected_cv = "data_set/expected_cv.json"

    for position in os.listdir(poistion_folder):
        user_interface = utils.LLMTesting(
            cv_file=cv_file,
            profile_file=expected_cv,
            poistion_file=os.path.join(poistion_folder, position),
            how_to_act=["Be truthful, don't invent any information."],
        )

        pipeline.execute(user_interface)

        user_interface.wrap_up(uuid=position.split(".")[0])
