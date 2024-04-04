import os
import cv2
from paddleocr import PPStructure,save_structure_res
from paddleocr.ppstructure.recovery.recovery_to_doc import sorted_layout_boxes, convert_info_docx

# Initialize PPStructure
# table_engine = PPStructure(recovery=True, use_gpu=False)
#
# # Define paths
# input_folder = '../2020_pdf_test/imgs'
# output_folder = '../2020_pdf_test/txt_2020_paddle'
#
# # Create output folder if it doesn't exist
# os.makedirs(output_folder, exist_ok=True)
#
# # Process each image in the input folder
# for img_name in os.listdir(input_folder):
#     if img_name.endswith('.png') or img_name.endswith('.jpg'):
#         img_path = os.path.join(input_folder, img_name)
#         img = cv2.imread(img_path)
#         if img is None:
#             print(f"Error: Unable to read image {img_path}")
#             continue
#
#         # Process the image
#         madori_test_data = table_engine(img)
#
#         # Save structure madori_test_data
#         save_structure_res(madori_test_data, output_folder, os.path.splitext(img_name)[0])
#
#         # Remove 'img' key from madori_test_data
#         for line in madori_test_data:
#             line.pop('img', None)
#
#         # Get image dimensions
#         h, w, _ = img.shape
#
#         # Sort layout boxes and convert to docx
#         res = sorted_layout_boxes(madori_test_data, w)
#         convert_info_docx(img, res, output_folder, os.path.splitext(img_name)[0])
table_engine = PPStructure(recovery=True, use_gpu=False)
# English image
# table_engine = PPStructure(recovery=True, lang='en')

save_folder = '../2020_pdf_test/txt_2020_paddle'
img_path = '../2020_pdf_test/imgs/page_33_page_1.png'
img = cv2.imread(img_path)
result = table_engine(img)
save_structure_res(result, save_folder, os.path.basename(img_path).split('.')[0])

for line in result:
    line.pop('img')
    print(line)

h, w, _ = img.shape
res = sorted_layout_boxes(result, w)
convert_info_docx(img, res, save_folder, os.path.basename(img_path).split('.')[0])