import os
from PyPDF2 import PdfReader, PdfWriter
def extract_pages(input_pdf, output_folder):
    try:
        # Create output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Open the input PDF file
        with open(input_pdf, "rb") as file:
            reader = PdfReader(file)

            # Iterate through each page and extract it
            for page_num, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)

                # Construct output file name
                output_file = os.path.join(output_folder, f"page_{page_num + 1}.pdf")

                # Write the extracted page to a new PDF file
                with open(output_file, "wb") as output_pdf:
                    writer.write(output_pdf)
                print(f"Page {page_num + 1} extracted and saved as {output_file}")

        print("Extraction successful.")
    except Exception as e:
        print(f"Error: {e}")

# Call the function with the desired input and output folders
pdf_file = './all/2020.pdf'
output_folder = './all/2020'

extract_pages(pdf_file, output_folder)