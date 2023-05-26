from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from PIL import Image
import os


def create_pdf(pdf_file, png_folder):
    c = canvas.Canvas(pdf_file, pagesize=landscape(A4))
    temp = []

    for filename in os.listdir(png_folder):
        if filename.endswith(".png"):
            temp.append(filename)

    files = sorted(temp)

    for filename in files:
        print(filename)
        file_path = os.path.join(png_folder, filename)
        img = Image.open(file_path)
        c.drawImage(file_path, 0, 0, width=A4[1], height=A4[0], preserveAspectRatio=True)
        c.showPage()

    c.save()

pdf_file = "data_files/attachment_#1.pdf"
png_folder = "data_files/"
create_pdf(pdf_file, png_folder)
