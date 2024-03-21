import os
import cv2
from paddleocr import save_structure_res
from paddleocr.ppstructure.recovery.recovery_to_doc import sorted_layout_boxes, convert_info_docx
from paddleocr import PPStructure, draw_structure_result
from PIL import Image



# def process_images(input_folder, output_folder):
#     # Create the output folder if it doesn't exist
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)
#
#     # Initialize PaddleOCR structure analysis engine
#     table_engine = PPStructure(recovery=True, use_gpu=False)
#     # English image
#     # table_engine = PPStructure(recovery=True, lang='en')
#
#     # Loop through each image file in the input folder
#     for image_file in os.listdir(input_folder):
#         # Check if the file is an image
#         if image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
#             # Construct the full path to the image file
#             img_path = os.path.join(input_folder, image_file)
#
#             # Read the image
#             img = cv2.imread(img_path)
#
#             # Perform structure analysis using PaddleOCR
#             result = table_engine(img)
#
#             # Save the structure analysis result
#             save_structure_res(result, output_folder, os.path.splitext(image_file)[0])
#
#             # Get image dimensions
#             h, w, _ = img.shape
#
#             # Sort layout boxes
#             res = sorted_layout_boxes(result, w)
#
#             # Convert structure analysis result to DOCX
#             convert_info_docx(img, res, output_folder, os.path.splitext(image_file)[0])
#
# # Input and output folder paths
# input_folder_path = "./2020_pdf_test/imgs"
# output_folder_path = "./output"
#
# # Process images in the input folder and save the results in the output folder
# process_images(input_folder_path, output_folder_path)
#


import os
import cv2
from paddleocr import PPStructure,save_structure_res
from paddleocr.ppstructure.recovery.recovery_to_doc import sorted_layout_boxes, convert_info_docx

# Chinese image
table_engine = PPStructure(recovery=True, use_gpu=False)
# English image
# table_engine = PPStructure(recovery=True, lang='en')

save_folder = './output'
img_path = './2020_pdf_test/imgs/page_56_page_1.png'
img = cv2.imread(img_path)
result = table_engine(img)
save_structure_res(result, save_folder, os.path.basename(img_path).split('.')[0])

for line in result:
    line.pop('img')
    print(line)

h, w, _ = img.shape
res = sorted_layout_boxes(result, w)
convert_info_docx(img, res, save_folder, os.path.basename(img_path).split('.')[0])