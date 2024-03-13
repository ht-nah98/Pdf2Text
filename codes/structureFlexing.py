import cv2
import numpy as np
from paddleocr import PPStructure


class PdfProcessor:
    def __init__(self):
        """
        Initialize PdfProcessor with PPStructure engine.
        """
        self.table_engine = PPStructure(recovery=True, use_gpu=False)

    def calculate_iou(self, box1, box2):
        """
        Calculate the Intersection over Union (IoU) of two bounding boxes.
        """
        x1, y1, w1, h1 = box1
        x2, y2, w2, h2 = box2

        # Calculate coordinates of intersection
        x_left = max(x1, x2)
        y_top = max(y1, y2)
        x_right = min(x1 + w1, x2 + w2)
        y_bottom = min(y1 + h1, y2 + h2)

        if x_right < x_left or y_bottom < y_top:
            return 0.0

        # Calculate area of intersection
        intersection_area = (x_right - x_left) * (y_bottom - y_top)

        # Calculate area of each bounding box
        box1_area = w1 * h1
        box2_area = w2 * h2

        # Calculate IoU
        iou = intersection_area / float(box1_area + box2_area - intersection_area)
        return iou

    # def print_and_extract_bboxes(self, column):
    #     bboxes = [bbox['bbox'] for bbox in column]
    #     return bboxes
    def process_structure(self, image_path):
        """
        Process the given image path.

        Args:
            image_path (str): Path to the image file.

        Returns:
            Tuple: A tuple containing result_sorted, left_part, and right_part.
        """
        # Read the image
        img = cv2.imread(image_path)

        # Process the image
        result = self.table_engine(img)
        image_height, image_width, _ = img.shape

        # Sort the result based on the position of the bounding boxes
        sorted_result = sorted(result, key=lambda x: (x['bbox'][1], x['bbox'][0]))

        # Remove duplicate bounding boxes
        cleaned_result = []
        for line in sorted_result:
            bbox = line['bbox']
            is_duplicate = False
            for other_line in cleaned_result:
                other_bbox = other_line['bbox']
                # Calculate IoU between the current bbox and other bbox
                iou = self.calculate_iou(bbox, other_bbox)
                if iou > 0.95:  # If IoU exceeds 95%, consider them as duplicates
                    is_duplicate = True
                    break
            if not is_duplicate:
                cleaned_result.append(line)
        # Determine column boundaries
        column_width = image_width / 3
        left_column_boundary = column_width
        middle_column_boundary = column_width * 2

        # Split the cleaned result into three lists: left_column, middle_column, and right_column
        left_column = []
        middle_column = []
        right_column = []

        for line in cleaned_result:
            line.pop('img')
            central_x = (line['bbox'][0] + line['bbox'][2]) / 2
            if central_x < left_column_boundary:
                left_column.append(line)
            elif central_x < middle_column_boundary:
                middle_column.append(line)
            else:
                right_column.append(line)
        # print('left_full_structure', left_column)
        # print('mid_full_structure', middle_column)
        # print('right_full_structure', right_column)

        all_columns = left_column + middle_column + right_column
        # Sort the combined list based on the y-coordinate (second element)
        all_columns.sort(key=lambda x: x['bbox'][1])
        # Group elements with similar y values within a threshold
        threshold = 10
        groups = []
        current_group = [all_columns[0]]
        for bbox in all_columns[1:]:
            if abs(bbox['bbox'][1] - current_group[-1]['bbox'][1]) <= threshold:
                current_group.append(bbox)
            else:
                groups.append(current_group)
                current_group = [bbox]
        groups.append(current_group)

        # Sort each group based on x-coordinate
        sorted_groups = [sorted(group, key=lambda x: x['bbox'][0]) for group in groups]

        # Flatten the sorted groups to get the final sorted result
        sorted_result = [bbox for group in sorted_groups for bbox in group]

        return sorted_result

# Example usage:
# processor = PdfProcessor()
# img_path = '../pages/testpage_idx3.png'
# result_sorted = processor.process_structure(img_path)
#
# for line in result_sorted:
#     if 'img' in line:
#         line.pop('img')
#     print(line)