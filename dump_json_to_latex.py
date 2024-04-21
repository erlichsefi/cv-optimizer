import os
import json
import platform
import subprocess
from openai import OpenAI


def get_user_cv_data(user_json_filename):
    with open(user_json_filename, "r") as file:
        return json.load(file)


def get_expected_latex_format(tex_filename):
    with open(tex_filename, "r") as file:
        return file.read()


def get_user_latex_file(tex_filename):
    with open(tex_filename, "r") as file:
        return file.read()


def dump_latex_to_file(user_latex, user_latex_filename):
    with open(user_latex_filename, "w") as file:
        file.write(user_latex)


def get_compliation(system_message, user_input, api_key, model="gpt-3.5-turbo"):
    client = OpenAI(api_key=api_key)
    stream = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input},
        ],
        temperature=0,
        stream=False
    )
    return stream


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


def have_a_look(image_path, prompt, api_key, model="gpt-4-vision-preview"):
    import requests

    def file_to_bytes(image_path):
        import base64

        """convert file to byte array"""

        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    base64_image = file_to_bytes(image_path)

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        "max_tokens": 300,
    }
    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    ).json()

    return response["choices"][0]["message"]["content"]


def compile_latex(tex_filename):
    filename, _ = os.path.splitext(tex_filename)
    # the corresponding PDF filename
    pdf_filename = filename + ".pdf"

    # compile TeX file
    # brew install basictex
    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", tex_filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # check if PDF is successfully generated
    if not os.path.exists(pdf_filename):
        error_message  = "process output:" + result.stdout.decode().split("Runaway argument?")[1]
        raise RuntimeError(f"PDF output not found. Error message: {error_message}")
    return pdf_filename

def extract_response(generations):
    string = generations.choices[0].message.content
    return string.split("```latex")[1].split("```")[0]
    

if __name__ == "__main__":

    user_cv_data = get_user_cv_data("user_cv.json")
    expected_format = get_expected_latex_format("cv.tex")
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
                    api_key=os.environ['OPENAI_API_KEY'])

    
    dump_latex_to_file(extract_response(generations),"user_tex.tex")

    tex_filename = "user_tex.tex"
    pdf_filename = None
    for _ in range(3):
        try:
            pdf_filename = compile_latex(tex_filename)
            break
        except RuntimeError as e:
            latex_file_content = get_user_latex_file(tex_filename) #assert latex_file_content == extract_response(generations)
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
                    """,
                    api_key=os.environ['OPENAI_API_KEY'])
            dump_latex_to_file(extract_response(generations),"user_tex.tex")

    if not pdf_filename:
        pdf_filename = compile_latex("user_tex.tex")


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
