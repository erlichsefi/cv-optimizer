
def extract_1(filename):
    from pdfminer.high_level import extract_text

    return extract_text(filename)


def extract_2(filename):
    # from PyPDF2 import PdfReader
    from pypdf import PdfReader

    text = ""
    with open(filename, "rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_3(file_name):
    import pdfplumber

    with pdfplumber.open(file_name) as pdf:
       text = ""
       for page in pdf.pages:
           text = f"{page.extract_text()}\n{text}"
       return text.replace("(cid:123)","")


def get_data_from_pdf(filename):

    if isinstance(filename, str):
        return extract_3(filename)
    else:
        from tempfile import NamedTemporaryFile

        with NamedTemporaryFile(dir=".", suffix=".pdf") as f:
            f.write(filename.getbuffer())
            return extract_3(f.name)