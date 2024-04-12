import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
import dotenv
from openai import OpenAI

dotenv.load_dotenv(".env")
def extract_text_from_pdf(file):
    from tempfile import NamedTemporaryFile

    with NamedTemporaryFile(dir='.', suffix='.pdf') as f:
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

def call_open_ai(prompt, model="gpt-3.5-turbo"):

    client = OpenAI()

    stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=False,
    )
    return stream.choices[0].message.content

def main():
    st.title("CV optimater")

    uploaded_file = st.file_uploader("Upload your current CV", type="pdf")

    position = st.text_area("The poistion copied details:")

    #st.text_area("The prompt",value=
prompt = """
Task Description:
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
    """)

    if st.button("Optimize my CV!"):
        cv_text = extract_text_from_pdf(uploaded_file)
        
        if cv_text.strip():
            word_count = call_open_ai(prompt.format(position=position,cv_text=cv_text))
            st.write(word_count)
        else:
            st.warning("Error when reading the CV")

if __name__ == "__main__":
    main()
