
from PIL import Image
import numpy as np
from pdf2image import convert_from_path
import tqdm
import os
from codes.tableFigureConverter import TableFigureExtractor
# from codes.pdfStructureAnalysis import PdfProcessor
# from codes.structureWith2Column import PdfProcessor
from codes.structureWith3column import PdfProcessor

# def pdf_to_images(pdf_path, output_folder):
#     """
#     Convert a PDF to images and save them in the output folder.
#
#     Args:
#         pdf_path (str): Path to the PDF file.
#         output_folder (str): Path to the folder where the images will be saved.
#     """
#     # Create the output folder if it doesn't exist
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)
#
#     # Convert each page of the PDF to an image
#     pages = convert_from_path(pdf_path)
#     for page in pages:
#         # Save the image with a suitable filename
#         image_path = os.path.join(output_folder, f"page.png")
#         page.save(image_path, 'PNG')
#
#
# # Example usage:
# pdf_path = './all/text_5.pdf'  # Path to your PDF file
# output_folder = './all'  # Folder where the images will be saved
# pdf_to_images(pdf_path, output_folder)


def process_result_sorted(result_sorted, img_path):
    def process_region(img, bbox, file):
        region = img.crop(bbox)
        region_np = np.array(region.convert("RGB"))
        table_extractor = TableFigureExtractor(region_np, lang='en', use_gpu=False)
        table_extractor.img_or_region = region_np
        boxes, probs, texts = table_extractor.extract_text()
        image_height, image_width, _ = region_np.shape
        horiz_box, verti_box = table_extractor.detect_boxes(boxes, image_width, image_height)
        horiz_lines = table_extractor.perform_non_max_suppression(np.array(horiz_box), np.array(probs))
        verti_lines = table_extractor.perform_non_max_suppression(np.array(verti_box), np.array(probs))
        out_array = table_extractor.fill_grid_structure(horiz_lines, verti_lines, boxes, texts, verti_box, horiz_box)
        table_extractor.write_to_txt(out_array, file, separator='|')
        file.write('\n')  # Add a newline character to insert a break

    with open("txt_generate/testpage_idx3.txt", "a", encoding="utf-8") as file:
        for line in result_sorted:
            if line['type'] == 'text' or line['type'] == 'reference' or line['type'] == 'title' or line['type'] == 'footer' or line['type'] == 'figure_caption':
                if isinstance(line['res'], list):
                    text_lines = [res['text'] for res in line['res']]
                    text = ' '.join(text_lines)
                    file.write(text + "\n")
                else:
                    file.write(line['res'] + "\n")
            elif line['type'] == 'table':
                table_regions = [line['bbox']]
                img = Image.open(img_path)
                for bbox in table_regions:
                    process_region(img, bbox, file)
            elif line['type'] == 'figure':
                figure_regions = [line['bbox']]
                img = Image.open(img_path)
                for bbox in figure_regions:
                    process_region(img, bbox, file)
            else:
                file.write("\n")

# Usage example:
processor = PdfProcessor()
# img_path = './all/page28-2011-v2.png'
img_path = 'pages/testpage_idx3.png'
result_sorted = processor.process_structure(img_path)
process_result_sorted(result_sorted, img_path)

for line in result_sorted:
    if 'img' in line:
        line.pop('img')
    print(line)





