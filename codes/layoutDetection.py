import os
import cv2
from paddleocr import PPStructure, draw_structure_result,save_structure_res
from PIL import Image
import numpy as np


table_engine = PPStructure(recovery=True, use_gpu=False)

img_path = '../imgTestv1/img2Cols/text_10.jpg'
save_directory = './generate_imgs'
img = cv2.imread(img_path)
# Get the width and height of the image
image_height, image_width, _ = img.shape

result = table_engine(img)
save_folder = '../all/structure'
save_structure_res(result, save_folder,os.path.basename(img_path).split('.')[0])
# Sort the result based on the position of the bounding boxes
sorted_result = sorted(result, key=lambda x: (x['bbox'][1], x['bbox'][0]))

x_cordinate = []
for line in sorted_result:
    line.pop('img')
    x_cordinate.append(line['bbox'][0])
    print(line)

x_cordinate = sorted(x_cordinate)
print(x_cordinate)

font_path = '../fonts/simfang.ttf' # font provided in PaddleOCR
image = Image.open(img_path).convert('RGB')
im_show = draw_structure_result(image, result,font_path=font_path)
im_show = Image.fromarray(im_show)

# Extract filename without extension
filename_without_extension = os.path.splitext(os.path.basename(img_path))[0]

# Save the image using os.path.join()
im_show.save(os.path.join(save_directory, filename_without_extension + '.jpg'))




