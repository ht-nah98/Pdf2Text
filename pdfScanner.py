import os
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTLine, LTRect, LTTextLineHorizontal
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tqdm import tqdm
from PyPDF2 import PdfReader, PdfWriter

# for page_layout in extract_pages("./Test/text_5.pdf"):
#     for element in page_layout:
#         print(element)
#         if isinstance(element, LTTextContainer):
#             print('haha', element.get_text())

from PIL import Image

# def png_to_pdf(png_file, pdf_file):
#     try:
#         image = Image.open(png_file)
#         # Convert RGBA images (with transparency) to RGB
#         if image.mode == 'RGBA':
#             image = image.convert('RGB')
#         image.save(pdf_file, "PDF", resolution=100.0)
#         print(f"Conversion successful: {png_file} converted to {pdf_file}")
#     except Exception as e:
#         print(f"Error: {e}")

# Example usage:
# png_to_pdf("./all/2016/page_19.pdf", "./all/page_27-2003.pdf")

def draw_bounding_boxes(pdf_path, page_num, output_pdf_path):
    # Get the page layout
    page_layout = next(extract_pages(pdf_path, page_numbers=[page_num-1]))

    # Create a canvas to draw the bounding boxes
    c = canvas.Canvas(output_pdf_path, pagesize=letter)

    # Draw bounding boxes around text elements
    for element in page_layout:
        if isinstance(element, LTTextContainer):
            # print('haha', element.get_text())
            for text_line in element:
                try:
                    x0 = text_line.x0
                    y0 = text_line.y0
                    width = text_line.width
                    height = text_line.height
                except AttributeError:
                    # Skip if x0, y0, width, or height attributes are not found
                    continue
                c.rect(x0, y0, width, height)
                # Optionally label each box
                # c.drawString(x0, y0 - 10, f"Box: ({x0}, {y0})")


        elif isinstance(element, (LTLine, LTRect)):

            # Draw rectangles for LTLine and LTRect elements
            c.rect(element.x0, element.y0, element.width, element.height)

    # Save the canvas as a PDF
    c.showPage()
    c.save()

# # Example usage:
# draw_bounding_boxes("./Test/text_5.pdf", 1, "./all/output_with_bounding_boxes4.pdf")

def extract_text_from_pdfs(pdf_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over PDF files in the input folder
    for pdf_file in tqdm(os.listdir(pdf_folder), desc="Processing PDFs", unit="file"):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, pdf_file)
            output_file = os.path.join(output_folder, os.path.splitext(pdf_file)[0] + ".txt")

            with open(output_file, "w", encoding="utf-8") as f_out:
                for page_layout in extract_pages(pdf_path):
                    for element in page_layout:
                        if isinstance(element, LTTextContainer):
                            text = element.get_text()
                            lines = text.strip().split('\n')  # Split text into lines
                            valid_lines = [line for line in lines if
                                           len(line.strip()) > 1]  # Filter lines with more than one character
                            if valid_lines:  # Check if there are valid lines
                                f_out.write(text)



# def extract_pages(input_pdf, output_folder):
#     try:
#         # Create output folder if it doesn't exist
#         if not os.path.exists(output_folder):
#             os.makedirs(output_folder)
#
#         # Open the input PDF file
#         with open(input_pdf, "rb") as file:
#             reader = PdfReader(file)
#
#             # Iterate through each page and extract it
#             for page_num, page in enumerate(reader.pages):
#                 writer = PdfWriter()
#                 writer.add_page(page)
#
#                 # Construct output file name
#                 output_file = os.path.join(output_folder, f"page_{page_num + 1}.pdf")
#
#                 # Write the extracted page to a new PDF file
#                 with open(output_file, "wb") as output_pdf:
#                     writer.write(output_pdf)
#                 print(f"Page {page_num + 1} extracted and saved as {output_file}")
#
#         print("Extraction successful.")
#     except Exception as e:
#         print(f"Error: {e}")
# Call the function with the desired input and output folders
pdf_folder = "./Test"
output_folder = "./Test/ResultTest"
# pdf_file = './all/2023_txt.pdf'
# Example usage:
# extract_pages(pdf_file, pdf_folder)
extract_text_from_pdfs(pdf_folder, output_folder)
# from pdfminer.high_level import extract_text
# import re
# import pandas as pd
# import parse
# import pdfplumber
# from collections import namedtuple
# Line = namedtuple('Line', 'company_id company_name doctype reference currency voucher inv_date due_date open_amt_tc open_amt_bc current months1 months2 months3')
# company_re = re.compile(r'(V\d+) (.*) Phone:')
# line_re = re.compile(r'\d{2}/\d{2}/\d{4} \d{2}/\d{2}/\d{4}')
# lines = []
# total_check = 0
# file = './all/2003/page_3.pdf'
# pdf = pdfplumber.open(file)
# p0 = pdf.pages[0]
# im = p0.to_image()
# print(im)
# table = p0.extract_table()
# print(table)