import os
import cv2
from paddleocr import PPStructure,draw_structure_result,save_structure_res

table_engine = PPStructure(recovery=True, use_gpu=False)


img_path = '../all/page_28-2011.png'
img = cv2.imread(img_path)
result = table_engine(img)
datas = []
for line in result:
    line.pop('img')
    # print(line['res'])
    for data in line['res']:
        datas.append(data)

# Sort data based on the y-coordinate of the first point in the text_region
sorted_data = sorted(datas, key=lambda x: x['text_region'][0][1])

# # Print the sorted data
# for item in sorted_data:
#     print(item)


def process_structure(image_path, datas):
    """
    Process the given image path.

    Args:
        image_path (str): Path to the image file.

    Returns:
        Tuple: A tuple containing result_sorted, left_part, and right_part.
    """
    # Read the image
    img = cv2.imread(image_path)
    image_height, image_width, _ = img.shape

    # Split the cleaned result into two lists: left_column and right_column
    left_column = [line for line in datas if line['text_region'][0][0] < image_width // 2]
    right_column = [line for line in datas if line['text_region'][1][0] > image_width // 2]

    # Combine the sorted left_column and right_column
    sorted_result = left_column + right_column
    return sorted_result



result = process_structure(img_path, sorted_data)
print(result)


# Open a file for writing
with open('output.txt', 'w') as file:
    # Iterate over each dictionary in the list
    for item in result:
        # Write the 'text' field to the file
        file.write(item['text'] + '\n')

# from PIL import Image
#
# font_path = '../fonts/simfang.ttf' # PaddleOCR下提供字体包
# image = Image.open(img_path).convert('RGB')
# im_show = draw_structure_result(image, result,font_path=font_path)
# im_show = Image.fromarray(im_show)
# im_show.save('result.jpg')








































