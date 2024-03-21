import os
import cv2
from paddleocr import save_structure_res
from paddleocr.ppstructure.recovery.recovery_to_doc import sorted_layout_boxes, convert_info_docx
from paddleocr import PPStructure, draw_structure_result
from PIL import Image


def convert_images_to_docx(input_folder, output_folder):
    # Initialize the table engine
    table_engine = PPStructure(recovery=True, use_gpu=False)

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through each image in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(input_folder, filename)

            # Read the image
            img = cv2.imread(img_path)

            # Process the image
            result = table_engine(img)

            # Remove 'img' key from result
            for line in result:
                line.pop('img')

            # Sort layout boxes
            h, w, _ = img.shape
            res = sorted_layout_boxes(result, w)

            # Convert to DOCX
            output_filename = os.path.splitext(filename)[0] + '.docx'
            convert_info_docx(img, res, output_folder, output_filename)

            print(f"Converted {filename} to DOCX.")

# Specify input and output folders
input_folder = './2020_pdf_test/imgs'
output_folder = './2020_pdf_test/txt_2020_paddle'

# Convert images to DOCX
convert_images_to_docx(input_folder, output_folder)





# def process_images(input_folder, output_folder, font_path):
#     # Initialize the table engine
#     table_engine = PPStructure(show_log=True, use_gpu=False)
#
#     # Create the output folder if it doesn't exist
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)
#
#     # Loop through each image in the input folder
#     for filename in os.listdir(input_folder):
#         if filename.endswith(('.png', '.jpg', '.jpeg')):
#             # Read the image
#             img_path = os.path.join(input_folder, filename)
#             img = cv2.imread(img_path)
#
#             # Process the image
#             result = table_engine(img)
#
#             # Remove 'img' key from result
#             for line in result:
#                 line.pop('img')
#
#             # Draw the result on the image and save
#             image = Image.open(img_path).convert('RGB')
#             im_show = draw_structure_result(image, result, font_path=font_path)
#             im_show = Image.fromarray(im_show)
#             result_path = os.path.join(output_folder, filename.replace('.png', '_result.jpg'))
#             im_show.save(result_path)
#             print(f"Processed: {filename}, Result saved: {result_path}")
#
#
# # Specify input and output folders and font path
# input_folder = './2020_pdf_test'
# output_folder = './2020_pdf_test/bbox_2020_paddle'
# font_path = './fonts/simfang.ttf'
#
# # Process images
# process_images(input_folder, output_folder, font_path)