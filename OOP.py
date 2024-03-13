
from PIL import Image
import numpy as np
from codes.tableFigureConverter import TableFigureExtractor
from codes.pdfStructureAnalysis import PdfProcessor
from pdf2image import convert_from_path
import os
from tqdm import tqdm



# def process_all_pages(input_folder, output_file):
#     with open(output_file, "a") as file:
#         # Get the list of PNG files in the input folder
#         png_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]
#
#         # Iterate over all PNG files with tqdm progress tracking
#         for filename in tqdm(png_files, desc="Processing PNG files"):
#             img_path = os.path.join(input_folder, filename)
#
#             try:
#                 # Process the image using PdfProcessor
#                 processor = PdfProcessor()
#                 result_sorted, _, _ = processor.process_image(img_path)
#
#                 # Process the result_sorted using process_result_sorted
#                 process_result_sorted(result_sorted, file)  # Remove the unnecessary img_path argument
#
#             except Exception as e:
#                 print(f"Error processing {img_path}: {e}")
#                 continue  # Skip to the next image file
#
# # Example usage:
# input_folder = './all_pages'  # Folder containing the PNG images
# output_file = 'data_full_1.txt'  # Output file where the processed data will be saved
# process_all_pages(input_folder, output_file)

import os
import cv2
from paddleocr import PPStructure,save_structure_res
from paddleocr.ppstructure.recovery.recovery_to_doc import sorted_layout_boxes, convert_info_docx

# Chinese image
table_engine = PPStructure(recovery=True, use_gpu=False)
# English image
# table_engine = PPStructure(recovery=True, lang='en')

save_folder = './txt_generate'
img_path = './pages/testpage_idx5.png'
img = cv2.imread(img_path)
result = table_engine(img)
save_structure_res(result, save_folder, os.path.basename(img_path).split('.')[0])

for line in result:
    line.pop('img')
    print(line)

h, w, _ = img.shape
res = sorted_layout_boxes(result, w)
convert_info_docx(img, res, save_folder, os.path.basename(img_path).split('.')[0])




