
import os
from pdf2image import convert_from_path

def pdf_to_images(pdf_path, output_folder):
    """
    Convert a PDF to images and save them in the output folder.

    Args:
        pdf_path (str): Path to the PDF file.
        output_folder (str): Path to the folder where the images will be saved.
    """
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Convert each page of the PDF to an image
    pages = convert_from_path(pdf_path)
    for page in pages:
        # Save the image with a suitable filename
        image_path = os.path.join(output_folder, f"page.png")
        page.save(image_path, 'PNG')


# Example usage:
pdf_path = './all/text_5.pdf'  # Path to your PDF file
output_folder = './all'  # Folder where the images will be saved
pdf_to_images(pdf_path, output_folder)







