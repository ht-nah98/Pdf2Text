import os
import cv2
import numpy as np
from paddleocr import PaddleOCR

class HouseStructure:
    def __init__(self, folder_path, ocr_lang='japan'):
        self.folder_path = folder_path
        self.ocr = PaddleOCR(use_angle_cls=True, lang=ocr_lang, use_gpu=False)

    def detect_text_boxes(self, img_path):
        madori_test_data = self.ocr.ocr(img_path, cls=True)
        text_boxes = []
        if madori_test_data[0] is None:
            print("No text detected in the image:", img_path)
            text_boxes.append([[0, 0], [0, 0], [0, 0], [0,0]])  # Return an empty list if no text is detected
        else:
            for line in madori_test_data:
                for word in line:
                    text_boxes.append(word[0])
        return text_boxes

    def create_text_mask(self, text_boxes, original_image):
        mask = np.zeros(original_image.shape[:2], dtype=np.uint8)
        for box in text_boxes:
            x_min, y_min = map(int, box[0])
            x_max, y_max = map(int, box[2])
            cv2.rectangle(mask, (x_min, y_min), (x_max, y_max), (255), cv2.FILLED)
        return mask

    def remove_text(self, img_path):
        original_image = cv2.imread(img_path)
        text_boxes = self.detect_text_boxes(img_path)
        text_mask = self.create_text_mask(text_boxes, original_image)
        madori_test_data = original_image.copy()
        madori_test_data[text_mask == 255] = (255, 255, 255)  # Fill text regions with white color
        return madori_test_data

    def preprocess_image(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 5, 22)
        kernel = np.ones((3, 3), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        dilated = cv2.dilate(binary, kernel, iterations=1)
        eroded = cv2.erode(dilated, kernel, iterations=1)
        edges = cv2.Canny(eroded, 50, 150)
        return edges

# Folder path containing images
folder_path = 'newyork/train_preprocess_img'
result_folder = './newyork/train_result_preprocess'

# Initialize HouseStructure object with the folder path
text_remover = HouseStructure(folder_path)

# Create madori_test_data folder if it doesn't exist
if not os.path.exists(result_folder):
    os.makedirs(result_folder)

# Process each image in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(('.jpg', '.png', '.jpeg')):  # Filter images based on extensions
        img_path = os.path.join(folder_path, filename)
        result_without_text = text_remover.remove_text(img_path)
        edge_image = text_remover.preprocess_image(result_without_text)

        # Save edge image to madori_test_data folder
        edge_image_path = os.path.join(result_folder, f'{os.path.splitext(filename)[0]}_pre.jpg')
        cv2.imwrite(edge_image_path, edge_image)  # Save edge_image directly













