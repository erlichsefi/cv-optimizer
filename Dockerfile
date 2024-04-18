# Use the Python 3.11 image from Microsoft's devcontainers as base
FROM python:3.11-bullseye

# Update package lists and install LaTeX
RUN apt-get update && apt-get install -y \
    texlive \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-lang-all \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# pdf2image
RUN apt-get install poppler-utils