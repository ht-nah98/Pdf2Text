import os
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTLine, LTRect, LTTextLineHorizontal
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tqdm import tqdm
import cv2
from pdfminer.high_level import extract_pages




def draw_bounding_boxes(pdf_path, page_num, output_pdf_path, output_txt_path):
    # Get the page layout
    page_layout = next(extract_pages(pdf_path, page_numbers=[page_num - 1]))

    # Create a canvas to draw the bounding boxes
    c = canvas.Canvas(output_pdf_path, pagesize=letter)

    # Open text file for writing bounding box information
    with open(output_txt_path, "w", encoding="utf-8") as txt_file:
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
                        text = text_line.get_text().strip()
                    except AttributeError:
                        # Skip if x0, y0, width, or height attributes are not found
                        continue

                    # Set line color to green
                    c.setStrokeColorRGB(0, 1, 0)  # Green color

                    # Draw rectangle border (bounding box)
                    c.rect(x0, y0, width, height)

                    # Add text related to the bounding box

                    # Set line color back to black (for text)
                    c.setStrokeColorRGB(0, 0, 0)  # Black color

                    c.drawString(x0, y0 - 10, text)

                    # Write bounding box information to text file
                    txt_file.write(f"Box: ({x0}, {y0}), Width: {width}, Height: {height}, Text: {text}\n")

            elif isinstance(element, (LTLine, LTRect, LTTextContainer)):
                # Draw rectangles for LTLine and LTRect elements
                c.rect(element.x0, element.y0, element.width, element.height)

    # Save the canvas as a PDF
    c.showPage()
    c.save()


def draw_bounding_boxes_for_folder(folder_path):
    output_folder_pdf = os.path.join(folder_path, "bbox_2020_pdfminer")
    output_folder_txt = os.path.join(folder_path, "box_position")
    os.makedirs(output_folder_pdf, exist_ok=True)
    os.makedirs(output_folder_txt, exist_ok=True)
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            input_pdf_path = os.path.join(folder_path, filename)
            output_pdf_path = os.path.join(output_folder_pdf, f"bbox_{filename}")
            output_txt_path = os.path.join(output_folder_txt, f"{filename.split('.')[0]}_page_1.txt")
            draw_bounding_boxes(input_pdf_path, 1, output_pdf_path, output_txt_path)

# Example usage:
draw_bounding_boxes_for_folder("./2020_pdf_test/pdf")




# def extract_text_from_pdfs(pdf_folder, output_folder):
#     # Create the output folder if it doesn't exist
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)
#
#     # Iterate over PDF files in the input folder
#     for pdf_file in tqdm(os.listdir(pdf_folder), desc="Processing PDFs", unit="file"):
#         if pdf_file.endswith(".pdf"):
#             pdf_path = os.path.join(pdf_folder, pdf_file)
#             output_file = os.path.join(output_folder, os.path.splitext(pdf_file)[0] + ".txt")
#
#             with open(output_file, "w", encoding="utf-8") as f_out:
#                 for page_layout in extract_pages(pdf_path):
#                     for element in page_layout:
#                         if isinstance(element, LTTextContainer):
#                             text = element.get_text()
#                             lines = text.strip().split('\n')  # Split text into lines
#                             valid_lines = [line for line in lines if
#                                            len(line.strip()) > 1]  # Filter lines with more than one character
#                             if valid_lines:  # Check if there are valid lines
#                                 f_out.write(text)






# output_folder_txt = "./2020_pdf_test/txt_2020_pdfminer"
# pdf_folder = "./2020_pdf_test"
# Example usage:
# extract_text_from_pdfs(pdf_folder, output_folder_txt)

# from PIL import Image
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
#
# # Read the bounding box data from the text file
# with open("2020_pdf_test/pdf/box_position/page_3_page_1.txt", "r", encoding="utf-8") as file:
#     bounding_boxes = file.readlines()
#
# # Load the PNG image
# image_path = "2020_pdf_test/imgs/page_3_page_1.png"
# image = Image.open(image_path)
#
# # Create figure and axes
# fig, ax = plt.subplots()
#
# # Display the image
# ax.imshow(image)
#
# # Draw bounding boxes on the image
# for box_info in bounding_boxes:
#     try:
#         # Check if the line contains the necessary information
#         if "Box:" in box_info and "Width:" in box_info and "Height:" in box_info and "Text:" in box_info:
#             # Extract bounding box coordinates and text
#             parts = box_info.strip().split(", ")
#             box = [float(coord.split(": ")[1].strip("()")) for coord in parts[:4]]
#             text = parts[-1].split(": ")[1][1:-1]  # Extracting text without quotes
#
#             # Create a rectangle patch
#             rect = patches.Rectangle((box[0], box[1]), box[2], box[3], linewidth=1, edgecolor='r', facecolor='none')
#
#             # Add the rectangle patch to the Axes
#             ax.add_patch(rect)
#
#             # Add text label
#             ax.text(box[0], box[1] - 10, text, fontsize=8, color='r')
#         else:
#             print("Skipping line:", box_info)
#     except Exception as e:
#         print("Error processing line:", box_info)
#         print("Error:", e)
#
# # Show the plot with bounding boxes
# plt.axis('off')
# plt.show()



