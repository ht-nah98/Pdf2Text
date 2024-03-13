import cv2
import numpy as np
import tensorflow as tf
from paddleocr import PaddleOCR

class TableExtractor:
    def __init__(self, img_path, lang='en', use_gpu=False):
        self.img_path = img_path
        self.lang = lang
        self.use_gpu = use_gpu

    def extract_text(self):
        img = cv2.imread(self.img_path)
        ocr = PaddleOCR(use_angle_cls=True, lang=self.lang, use_gpu=self.use_gpu)
        output = ocr.ocr(self.img_path)
        boxes = [line[0] for line in output[0]]
        probs = [line[1][1] for line in output[0]]
        texts = [line[1][0] for line in output[0]]
        return boxes, probs, texts

    def detect_boxes(self, boxes, image_width, image_height):
        horiz_box = []
        verti_box = []
        for box in boxes:
            x_h, y_h = 0, int(box[0][1])  # Start from left side and use y-coordinate for horizontal box
            width_h = image_width
            height_h = int(box[2][1] - box[0][1])  # Calculate height based on box coordinates
            horiz_box.append([x_h, y_h, x_h + width_h, y_h + height_h])

            x_v, y_v = int(box[0][0]), 0  # Start from top and use x-coordinate for vertical box
            width_v = int(box[2][0] - box[0][0])  # Calculate width based on box coordinates
            height_v = image_height
            verti_box.append([x_v, y_v, x_v + width_v, y_v + height_v])
        return horiz_box, verti_box

    def perform_non_max_suppression(self, box_tensor, probs_tensor):
        out = tf.image.non_max_suppression(
            box_tensor,
            probs_tensor,
            max_output_size=1000,
            iou_threshold=0.1,
            score_threshold=float('-inf'),
            name=None
        )
        return np.sort(np.array(out))

    def fill_grid_structure(self, horiz_lines, verti_lines, boxes, texts, verti_box, horiz_box):
        out_array = [["" for _ in range(len(verti_lines))] for _ in range(len(horiz_lines))]

        unordered_boxes = [verti_box[i][0] for i in verti_lines]
        ordered_boxes = np.argsort(unordered_boxes)

        for i in range(len(horiz_lines)):
            empty_cell = True
            for j in range(len(verti_lines)):
                resultant = self.intersection(horiz_box[horiz_lines[i]], verti_box[verti_lines[ordered_boxes[j]]])
                for b in range(len(boxes)):
                    the_box = [boxes[b][0][0], boxes[b][0][1], boxes[b][2][0], boxes[b][2][1]]
                    if self.iou(resultant, the_box) > 0.1:
                        out_array[i][j] = texts[b]
                        empty_cell = False
                if empty_cell:
                    out_array[i][j] = ""
        return out_array

    @staticmethod
    def intersection(box_1, box_2):
        return [box_2[0], box_1[1], box_2[2], box_1[3]]

    @staticmethod
    def iou(box_1, box_2):
        x1 = max(box_1[0], box_2[0])
        y1 = max(box_1[1], box_2[1])
        x2 = min(box_1[2], box_2[2])
        y2 = min(box_1[3], box_2[3])

        inter = abs(max((x2 - x1,0)) * max((y2-y1),0))
        if inter == 0:
            return 0

        box_1_area = abs((box_1[2] - box_1[0]) * (box_1[3] - box_1[1]))
        box_2_area = abs((box_2[2] - box_2[0]) * (box_2[3] - box_2[1]))

        return inter / float(box_1_area + box_2_area - inter)

    @staticmethod
    def write_to_txt(data, file_path, separator='|'):
        # Find the maximum length of each column
        max_lengths = [max(len(str(col)) for col in column) for column in zip(*data)]

        with open(file_path, 'w') as f:
            for row in data:
                formatted_row = [f"{col:{length}}{separator}" if col else '' for col, length in zip(row, max_lengths)]
                f.write('\t'.join(formatted_row) + '\n')

if __name__ == "__main__":
    # img_path = '../imgtest/unkonw/[8, 17, 1187, 645]_0.jpg'
    img_path = '../pages/testpage_idx4.png'
    image_cv = cv2.imread(img_path)

    image_height = image_cv.shape[0]
    image_width = image_cv.shape[1]

    table_extractor = TableExtractor(img_path, lang='en', use_gpu=False)
    boxes, probs, texts = table_extractor.extract_text()

    horiz_box, verti_box = table_extractor.detect_boxes(boxes, image_width, image_height)

    horiz_lines = table_extractor.perform_non_max_suppression(np.array(horiz_box), np.array(probs))
    verti_lines = table_extractor.perform_non_max_suppression(np.array(verti_box), np.array(probs))

    out_array = table_extractor.fill_grid_structure(horiz_lines, verti_lines, boxes, texts, verti_box, horiz_box)

    # Save data to a text file with separator and aligned columns
    table_extractor.write_to_txt(out_array, 'aligned_data1.txt', separator='|')