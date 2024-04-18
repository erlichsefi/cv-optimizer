



import os
import platform
import subprocess

def get_latex(tex_filename):
    with open(tex_filename,"r") as file:
        return file.read()


def create_csv(tex_filename):
    filename, _ = os.path.splitext(tex_filename)
    # the corresponding PDF filename
    pdf_filename = filename + '.pdf'

    # compile TeX file
    # brew install basictex
    subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_filename])

    # check if PDF is successfully generated
    if not os.path.exists(pdf_filename):
        raise RuntimeError('PDF output not found')

    # open PDF with platform-specific command
    if platform.system().lower() == 'darwin':
        subprocess.run(['open', pdf_filename])
    elif platform.system().lower() == 'windows':
        os.startfile(pdf_filename)
    elif platform.system().lower() == 'linux':
        subprocess.run(['xdg-open', pdf_filename])
    else:
        raise RuntimeError('Unknown operating system "{}"'.format(platform.system()))
    

if __name__ == "__main__":
    create_csv("cv.tex")