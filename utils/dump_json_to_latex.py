import json

from .interface import UserInterface,TerminalInterface
from .llm_store import get_compliation
from .filestore import get_all_position_cv_offers,get_expected_latex_format,set_user_latex_file,compile_user_latex,get_user_latex_file,move_pdf_to_created


def pdf_to_image(pdf_file, output_folder=None, output_format="png", dpi=200):
    from pdf2image import convert_from_path

    output_images = convert_from_path(
        pdf_file,
        output_folder=output_folder,
        output_file="output",
        fmt=output_format,
        dpi=dpi,
    )

    images = []
    for i, image in enumerate(output_images):
        tmp_image = f"page_{i+1}.jpeg"
        image.save(tmp_image, "JPEG")
        images.append(tmp_image)
    return images

    

def json_to_pdf(user_cv_data):
    expected_format = get_expected_latex_format()
    generations = get_compliation(system_message=f"""
                    Given the user data, fill the latex format with the user details.
                                  
                    Here is an example of the latex content:
                    {expected_format}

                    You need to:
                        - replace all '&' symbol in user details to the word 'and'
                    

                    Respond in the following format:
                    ```latex
                    // place your response here
                    ```
                    """,
                    user_input=json.dumps(user_cv_data,indent=4),
                    is_json_expected=False
                    
    )   
    set_user_latex_file(generations,extract_latex=True)

    
    pdf_filename = None
    for _ in range(3):
        try:
            pdf_filename = compile_user_latex()
            break
        except RuntimeError as e:
            latex_file_content = get_user_latex_file() #assert latex_file_content == extract_response(generations)
            generations = get_compliation(system_message=f"""
                    You are trying to compile a latex file.
                    You need to fix the issues raised by the compiling process.

                    Guideline:
                        - make minimal changes
                    ```latex
                    // place your the fixd latex here
                    ```
                                        """,
                                        user_input=f"""
                    Errors:
                    {e}

                    File content to fix:
                    {latex_file_content}
                    """)
            set_user_latex_file(generations,extract_latex=True)

    if not pdf_filename:
        pdf_filename = compile_user_latex()

    if pdf_filename:
        return move_pdf_to_created()
    return None
    
    
    

def run(user_interface:UserInterface):
    user_interface.send_user_message("Processing...")
    cv_offers = get_all_position_cv_offers()
    pdfs = []
    for offer in cv_offers:

        pdf = json_to_pdf(offer)
        if pdf:
            pdfs.append(pdf)
    
    user_interface.send_user_message("Here are the revised CVs:")
    user_interface.send_user_message("\n".join(pdfs))

    # pdf_filename = "user_tex.pdf"
    # if pdf_filename:
    #     latex_file_content = get_user_latex_file("user_tex.tex")
    #     pngs = pdf_to_image(pdf_filename)

    #     vision_fixs = have_a_look(
    #         pngs[0],
    #         prompt="""have a look on this pdf file screenshot, 
    #                 what are the fixes you need to make to the latex file that created this pdf?
    #                 is there text overlapping? is there text that is not in place? 
    #                 provide instructions.""",
    #         api_key=os.environ["OPENAI_API_KEY"],
    #     )
    #     generations = get_compliation(
    #         system_message="""
    #                 You are tring the issues provided to you by the user.
    #                 """,
    #         user_input=f"""
    #                 {latex_file_content}

    #                 you got the following istructions to fix:
    #                 {vision_fixs}
    #                 """,
    #         api_key=os.environ["OPENAI_API_KEY"],
    #     )
    #     dump_latex_to_file(generations.choices[0].message.content, "user_tex.tex")
    #     compile_latex("user_tex.tex")

if __name__ == "__main__":
    print(run())