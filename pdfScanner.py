import os
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTLine, LTRect, LTTextLineHorizontal
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tqdm import tqdm


# for page_layout in extract_pages("./all/2020/page_8.pdf"):
#     for element in page_layout:
#         print(element)
#         # if isinstance(element, LTTextContainer):
#         #     print('haha', element.get_text())





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

def draw_bounding_boxes_for_folder(folder_path):
    output_folder = os.path.join(folder_path, "bbox_2020_pdfminer")
    os.makedirs(output_folder, exist_ok=True)
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            input_pdf_path = os.path.join(folder_path, filename)
            output_pdf_path = os.path.join(output_folder, f"bbox_{filename}")
            draw_bounding_boxes(input_pdf_path, 1, output_pdf_path)

# Example usage:
# draw_bounding_boxes_for_folder("./2020_pdf_test")
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






output_folder_txt = "./2020_pdf_test/txt_2020_pdfminer"
pdf_folder = "./2020_pdf_test"
# Example usage:
extract_text_from_pdfs(pdf_folder, output_folder_txt)
