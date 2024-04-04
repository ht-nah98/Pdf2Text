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


# # Chinese image
# table_engine = PPStructure(recovery=True, use_gpu=False)
# # English image
# # table_engine = PPStructure(recovery=True, lang='en')
#
# save_folder = './txt_generate'
# img_path = './pages/testpage_idx5.png'
# img = cv2.imread(img_path)
# madori_test_data = table_engine(img)
# save_structure_res(madori_test_data, save_folder, os.path.basename(img_path).split('.')[0])
#
# for line in madori_test_data:
#     line.pop('img')
#     print(line)
#
# h, w, _ = img.shape
# res = sorted_layout_boxes(madori_test_data, w)
# convert_info_docx(img, res, save_folder, os.path.basename(img_path).split('.')[0])





































