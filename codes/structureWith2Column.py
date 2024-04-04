import cv2
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

        # Sort the madori_test_data based on the position of the bounding boxes
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

        # Split the cleaned madori_test_data into two lists: left_column and right_column
        left_column = [line for line in cleaned_result if line['bbox'][2] < image_width // 2]
        right_column = [line for line in cleaned_result if line['bbox'][0] > image_width // 2]

        # Combine the sorted left_column and right_column
        sorted_result = left_column + right_column

        # Move footer to the end
        footer_lines = [line for line in sorted_result if line['type'] == 'footer']
        sorted_result = [line for line in sorted_result if line['type'] != 'footer'] + footer_lines

        return sorted_result

# # Example usage:
# processor = PdfProcessor()
# img_path = './pages/testpage_idx6.png'
# result_sorted, left_part, right_part = processor.process_image(img_path)