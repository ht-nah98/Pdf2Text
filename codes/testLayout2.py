import os
import cv2
from paddleocr import PPStructure,draw_structure_result,save_structure_res

table_engine = PPStructure(recovery=True, use_gpu=False)


img_path = '../pages/testpage_idx4.png'
img = cv2.imread(img_path)
result = table_engine(img)
datas = []
for line in result:
    line.pop('img')
    # print(line['res'])
    for data in line['res']:
        datas.append(data)


from PIL import Image

font_path = '../fonts/simfang.ttf' # PaddleOCR下提供字体包
image = Image.open(img_path).convert('RGB')
im_show = draw_structure_result(image, result,font_path=font_path)
im_show = Image.fromarray(im_show)
im_show.save('result2.jpg')








































