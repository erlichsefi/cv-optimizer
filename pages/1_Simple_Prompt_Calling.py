import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
import os

from openai import OpenAI

st.set_page_config(page_title="Single Prompt")


def extract_text_from_pdf(file):
    from tempfile import NamedTemporaryFile

    with NamedTemporaryFile(dir=".", suffix=".pdf") as f:
        f.write(file.getbuffer())

        text = ""
        with open(f.name, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
        return text


def create_pdf_from_text(text):
    writer = PdfWriter()
    writer.add_page()
    writer.pages[0].append_text(text)
    output_pdf = BytesIO()
    writer.write(output_pdf)
    return output_pdf.getvalue()


def call_open_ai(prompt, api_key, model="gpt-3.5-turbo"):

    client = OpenAI(api_key=api_key)

    stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=False,
    )
    return stream.choices[0].message.content


def main():
    st.title("CV optimater using a singe prompt")

    prompt_value = """Task Description:
    You are tasked with optimizing a user's CV based on a given position description without revealing that the CV has been optimized or inventing information not present in the original CV.

    User CV:
    {cv_text}
                            
    Position Description:
    {position}
                            
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
        """
    prompt = st.text_area(
        "The prompt", value=prompt_value, height=int(len(prompt_value) / 2)
    )

    if st.button("Optimize my CV!"):
        # check if the CV was uploaded
        if (
            "uploaded_file" not in st.session_state
            or st.session_state["uploaded_file"] is None
        ):
            st.warning("Please upload your CV. (in the sidebar)")
            st.stop()

        # check if the position details was uploaded 
        if (
            "position" not in st.session_state
            or st.session_state["position"] is None
            and len(st.session_state["position"]) > 10
        ):
            st.warning("Please fill position details before moving on. (in the sidebar")
            st.stop()

        # check the prompt contains the placeholders
        if "{cv_text}" not in prompt or "{position}" not in prompt:
            st.warning(
                "Make sure the keep the holdplacers {position} and {cv_text} in your prompt."
            )
            st.stop()

        # extract user input
        cv_text = extract_text_from_pdf(st.session_state["uploaded_file"])
        position = st.session_state["position"]

        # get the api_key
        api_key = os.environ.get("OPENAI_API_KEY", None)
        if (
            "oai_key" not in st.session_state
            or st.session_state["oai_key"] is None
            or not st.session_state["oai_key"].startswith("sk")
        ):

            # register to google sheet if we keep the key myown 
            from streamlit_gsheets import GSheetsConnection

            conn = st.connection("gsheets", type=GSheetsConnection)
            all_cvs = conn.read(
                worksheet="CV",
                usecols=[0, 1, 2],
            ).dropna(axis=0)
            new_row = {
                "Unnamed: 0": position,
                "Unnamed: 1": cv_text,
                "Unnamed: 2": prompt,
            }
            all_cvs = all_cvs.append(new_row, ignore_index=True)
            conn.update(
                worksheet="CV",
                data=all_cvs,
            )
            st.toast("Calling OpenAI.")
        else:
            api_key = st.session_state["oai_key"]
            st.toast("Ok Ok... using your token")

        if cv_text.strip():
            response = call_open_ai(
                prompt.format(position=position, cv_text=cv_text), api_key=api_key
            )
            st.write(response)
        else:
            st.warning("Error when reading the CV")


if __name__ == "__main__":
    main()
