import cv2
from paddleocr import PPStructure


class PdfProcessor:
    def __init__(self):
        """
        Initialize PdfProcessor with PPStructure engine.
        """
        self.table_engine = PPStructure(recovery=True, use_gpu=False)

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

        # Define a custom key function to sort by y-coordinate first, then by x-coordinate
        def custom_key(item):
            return item['bbox'][1], item['bbox'][0]

        # Sort the madori_test_data list based on the custom key
        result_sorted = sorted(result, key=custom_key)

        return result_sorted

# # Example usage:
# processor = PdfProcessor()
# img_path = './pages/testpage_idx6.png'
# result_sorted, left_part, right_part = processor.process_image(img_path)