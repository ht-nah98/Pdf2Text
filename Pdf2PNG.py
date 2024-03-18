
import os
from pdf2image import convert_from_path
from PIL import Image
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


def png_to_pdf(png_file, pdf_file):
    try:
        image = Image.open(png_file)
        # Convert RGBA images (with transparency) to RGB
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        image.save(pdf_file, "PDF", resolution=100.0)
        print(f"Conversion successful: {png_file} converted to {pdf_file}")
    except Exception as e:
        print(f"Error: {e}")

# Example usage:
png_to_pdf("./all/2016/page_19.pdf", "./all/page_27-2003.pdf")




