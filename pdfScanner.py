import os
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBox, LTTextContainer, LTLine, LTRect, LTTextLineHorizontal
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tqdm import tqdm
import cv2
from pdf2image import convert_from_path
from PIL import ImageDraw

# Function to extract bounding box and text data
def extract_bbox_and_text(pdf_file):
    bbox_data = []
    text_data = []
    for page_layout in extract_pages(pdf_file):
        _, _, width, height = page_layout.bbox  # Extract page width and height
        for element in page_layout:
            if isinstance(element, LTTextBox):
                x0, y0, x1, y1 = element.bbox
                # Adjust y-coordinates to match PIL coordinate system
                adjusted_y0 = height - y1
                adjusted_y1 = height - y0
                bbox_data.append((x0, adjusted_y0, x1, adjusted_y1))
                text_data.append(element.get_text().strip())
    return bbox_data, text_data

# box, text = extract_bbox_and_text('2020_pdf_test/pdf/page_18.pdf')
# print(box)
# print(text)
def process_images(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get the list of image files in the input folder
    image_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

    # Process each image
    for image_file in image_files:
        # Path to the input image
        input_image_path = os.path.join(input_folder, image_file)

        # Path to save the annotated image
        output_image_path = os.path.join(output_folder, f"annotated_{image_file}")

        # Convert PDF to PNG
        images = convert_from_path(input_image_path)

        # Extract bounding box and text data
        bbox_data, text_data = extract_bbox_and_text(input_image_path)

        # Iterate over images (pages)
        for idx, image in enumerate(images):
            # Open the image and create a drawing object
            img_draw = ImageDraw.Draw(image)

            # Get the width and height of the image
            img_width, img_height = image.size

            # Extract page width and height from the first page of the PDF layout
            _, _, pdf_width, pdf_height = extract_pages(input_image_path).__next__().bbox

            # Iterate through bbox_data and draw rectangles and text
            for bbox, text in zip(bbox_data, text_data):
                # Adjust bounding box coordinates to match image scale
                x0 = bbox[0] * img_width / pdf_width
                y0 = bbox[1] * img_height / pdf_height
                x1 = bbox[2] * img_width / pdf_width
                y1 = bbox[3] * img_height / pdf_height
                adjusted_bbox = (x0, y0, x1, y1)

                # Draw rectangle
                img_draw.rectangle(adjusted_bbox, outline='red')
                # Add text
                img_draw.text((adjusted_bbox[0], adjusted_bbox[1]), text, fill='black')

            # Save the annotated image
            image.save(output_image_path.format(idx + 1))

# Input and output folder paths
input_folder_path = "./2020_pdf_test/pdf"
output_folder_path = "./2020_pdf_test/bbox_2020_pdfminer"

# Process images in the input folder and save annotated images in the output folder
process_images(input_folder_path, output_folder_path)


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






# output_folder_txt = "./2020_pdf_test/txt_2020_pdfminer"
# pdf_folder = "./2020_pdf_test"
# # Example usage:
# extract_text_from_pdfs(pdf_folder, output_folder_txt)

def extract_bbox_and_text(pdf_file):
    data = []
    for page_layout in extract_pages(pdf_file):
        _, _, width, height = page_layout.bbox  # Extract page width and height
        for element in page_layout:
            if isinstance(element, LTTextBox):
                bbox = element.bbox
                text = element.get_text().strip()
                # Calculate scaled bounding box values
                bbox_scale = (
                    bbox[0] / width,
                    bbox[1] / height,
                    bbox[2] / width,
                    bbox[3] / height
                )
                data.append({
                    'bbox': bbox,
                    'text': text,
                    'bbox_scale': bbox_scale
                })
    return data



print(extract_bbox_and_text('2020_pdf_test/pdf/page_18.pdf'))




