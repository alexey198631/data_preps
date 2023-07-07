import os
from pdf2docx import Converter

def convert_pdf_to_docx(pdf_path, docx_path):
    cv = Converter(pdf_path)
    cv.convert(docx_path, start=0, end=None)
    cv.close()

# Provide the paths for the PDF and output DOCX files
pdf_file = "test.pdf"
docx_file = "test.docx"

# Convert the PDF to DOCX
convert_pdf_to_docx(pdf_file, docx_file)

print("Conversion complete.")
