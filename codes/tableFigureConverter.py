import cv2
import numpy as np
import tensorflow as tf
from paddleocr import PaddleOCR


class TableFigureExtractor:
    def __init__(self, img_or_region, lang='en', use_gpu=False):
        """
        Initialize the TableFigureExtractor with the image or region to process.

        Args:
            img_or_region: Input image or region to process.
            lang (str): Language parameter for OCR.
            use_gpu (bool): Whether to use GPU for processing.
        """
        self.img_or_region = img_or_region
        self.lang = lang
        self.use_gpu = use_gpu

    def extract_text(self):
        """
        Extract text from the image or region using PaddleOCR.

        Returns:
            Tuple: Tuple containing lists of bounding boxes, probabilities, and texts.
        """
        if isinstance(self.img_or_region, str):  # Input is image path
            img = cv2.imread(self.img_or_region)
        else:  # Input is region
            img = self.img_or_region

        ocr = PaddleOCR(use_angle_cls=True, lang=self.lang, use_gpu=self.use_gpu)
        output = ocr.ocr(img)
        boxes = [line[0] for line in output[0]]
        probs = [line[1][1] for line in output[0]]
        texts = [line[1][0] for line in output[0]]
        return boxes, probs, texts

    def detect_boxes(self, boxes, image_width, image_height):
        """
        Detect horizontal and vertical boxes based on the bounding box coordinates.

        Args:
            boxes (list): List of bounding box coordinates.
            image_width (int): Width of the image.
            image_height (int): Height of the image.

        Returns:
            Tuple: Tuple containing lists of horizontal and vertical boxes.
        """
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
        """
        Perform non-maximum suppression to filter out overlapping boxes.

        Args:
            box_tensor: Tensor containing box coordinates.
            probs_tensor: Tensor containing probabilities.

        Returns:
            ndarray: Numpy array containing indices of the selected boxes.
        """
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
        """
        Fill the grid structure with text based on detected boxes and texts.

        Args:
            horiz_lines (list): List of horizontal lines.
            verti_lines (list): List of vertical lines.
            boxes (list): List of bounding boxes.
            texts (list): List of texts corresponding to the boxes.
            verti_box (list): List of vertical boxes.
            horiz_box (list): List of horizontal boxes.

        Returns:
            list: List representing the filled grid structure.
        """
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
        """
        Calculate the intersection of two bounding boxes.

        Args:
            box_1 (list): First bounding box coordinates.
            box_2 (list): Second bounding box coordinates.

        Returns:
            list: Intersection bounding box coordinates.
        """
        return [box_2[0], box_1[1], box_2[2], box_1[3]]

    @staticmethod
    def iou(box_1, box_2):
        """
        Calculate the Intersection over Union (IoU) between two bounding boxes.

        Args:
            box_1 (list): First bounding box coordinates.
            box_2 (list): Second bounding box coordinates.

        Returns:
            float: Intersection over Union (IoU) value.
        """
        x1 = max(box_1[0], box_2[0])
        y1 = max(box_1[1], box_2[1])
        x2 = min(box_1[2], box_2[2])
        y2 = min(box_1[3], box_2[3])

        inter = abs(max((x2 - x1, 0)) * max((y2 - y1), 0))
        if inter == 0:
            return 0

        box_1_area = abs((box_1[2] - box_1[0]) * (box_1[3] - box_1[1]))
        box_2_area = abs((box_2[2] - box_2[0]) * (box_2[3] - box_2[1]))

        return inter / float(box_1_area + box_2_area - inter)
    @staticmethod
    def write_to_txt(data, file_obj, separator='|'):
        """
        Write the table data to a text file with separator and aligned columns.

        Args:
            data (list): List of lists containing the table data.
            file_obj: File object to write the data.
            separator (str): Separator character between columns.
        """
        # Find the maximum length of each column
        max_lengths = [max(len(str(col)) for col in column) for column in zip(*data)]

        for row in data:
            formatted_row = [f"{col:{length}}{separator}" if col else '' for col, length in zip(row, max_lengths)]
            file_obj.write('\t'.join(formatted_row) + '\n')
