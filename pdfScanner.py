from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import os
# for page_layout in extract_pages("./all/2003/page_3.pdf"):
#     print(page_layout)
#     for element in page_layout:
#         print(element)
#         if isinstance(element, LTTextContainer):
#             print('haha', element.get_text())
pdf_folder = "./Test"
output_folder = "./Test/ResultTest"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Iterate over PDF files in the input folder
for pdf_file in os.listdir(pdf_folder):
    if pdf_file.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, pdf_file)
        output_file = os.path.join(output_folder, os.path.splitext(pdf_file)[0] + ".txt")

        with open(output_file, "w", encoding="utf-8") as f_out:
            for page_layout in extract_pages(pdf_path):
                for element in page_layout:
                    if isinstance(element, LTTextContainer):
                        text = element.get_text()
                        f_out.write(text)

# from pdfminer.high_level import extract_pages
# from pdfminer.layout import LTTextContainer
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
#
# def draw_bounding_boxes(pdf_path, page_num, output_pdf_path):
#     # Get the page layout
#     page_layout = next(extract_pages(pdf_path, page_numbers=[page_num-1]))
#
#     # Create a canvas to draw the bounding boxes
#     c = canvas.Canvas(output_pdf_path, pagesize=letter)
#
#     # Draw bounding boxes around text elements
#     for element in page_layout:
#         if isinstance(element, LTTextContainer):
#             for text_line in element:
#                 try:
#                     x0 = text_line.x0
#                     y0 = text_line.y0
#                     width = text_line.width
#                     height = text_line.height
#                 except AttributeError:
#                     # Skip if x0, y0, width, or height attributes are not found
#                     continue
#                 c.rect(x0, y0, width, height)
#
#     # Save the canvas as a PDF
#     c.showPage()
#     c.save()
#
# # Example usage:
# draw_bounding_boxes("./all/2006/page_13.pdf", 1, "./all/output_with_bounding_boxes3.pdf")

# import os
# from PyPDF2 import PdfReader, PdfWriter
#
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
#
# # Example usage:
# extract_pages("./all/2006.pdf", "./all/2006")

from PIL import Image
#
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
#
# # Example usage:
# png_to_pdf("./all/2016/page_19.pdf", "./all/page_27-2003.pdf")


def format_table(txt_file):
    with open(txt_file, "r") as f:
        lines = f.readlines()

    # Determine the number of columns
    max_columns = max(len(line.split()) for line in lines)

    # Initialize an empty table
    table = []

    # Split lines into columns
    for line in lines:
        columns = line.split()
        table.append(columns + [''] * (max_columns - len(columns)))

    # Transpose the table
    transposed_table = list(map(list, zip(*table)))

    # Calculate column widths
    column_widths = [max(len(cell) for cell in column) for column in transposed_table]

    # Format the table
    formatted_table = ''
    for row in table:
        formatted_row = ''
        for i, cell in enumerate(row):
            formatted_row += cell.ljust(column_widths[i] + 2)
        formatted_table += formatted_row.strip() + '\n'

    return formatted_table

# Example usage
txt_file = "./Test/ResultTest/text_6.txt"
formatted_table = format_table(txt_file)
print(formatted_table)