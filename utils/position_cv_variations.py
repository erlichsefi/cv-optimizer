
from llm_store import get_compliation
from filestore import get_completed_cv_data,get_cv_blueprint,get_position_data,set_position_cv_offers
import json



def run():
    position_data = get_position_data()
    cv_data = get_completed_cv_data()
    cv_blueprint = get_cv_blueprint()

    offers = get_compliation(system_message="",user_input=f"""Task Description:
    You are tasked with optimizing a user's CV based on a given position description without revealing that the CV has been optimized or inventing information not present in the original CV.

    User CV:
    {json.dumps(cv_data,indent=4)}
                            
    Position Description:
    {json.dumps(position_data,indent=4)}
                            
    Instructions:

    - Review the user's CV carefully.
    - Analyze the position description to understand the specific requirements and preferences of the role.
    - Enhance the user's CV by rephrasing, restructuring, or emphasizing existing information to better match the position description.
    - Ensure that any modifications made are subtle and do not give away the fact that the CV has been optimized.
    - Avoid inventing new information or embellishing existing details beyond what is provided in the original CV.

    Additional Guidance:

    - Focus on highlighting relevant experiences, skills, and achievements that directly correlate with the position requirements.
    - Use language that mirrors the tone and terminology used in the position description.
    - Maintain the overall format and style of the original CV to avoid suspicion of tampering.

    Outcome:
    - Your final output should be an optimized version of the user's CV that appears natural and cohesive while effectively addressing the expectations outlined in the position description.
    - Provide the response in markdown.

    Response format:
    ```json
    {json.dumps(cv_blueprint,indent=4)}
    ```
    """,
    is_json_expected=True,
    num_of_gen=2,
    temperature=0.1
    )
    set_position_cv_offers(offers)


if __name__ == "__main__":
    run()
















