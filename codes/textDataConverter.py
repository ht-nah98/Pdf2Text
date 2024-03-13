from paddleocr import PaddleOCR

class TextExtractor:
    def __init__(self, lang='en', use_gpu=False):
        self.ocr = PaddleOCR(use_angle_cls=True, lang=lang, use_gpu=use_gpu)

    def extract_text(self, img_path):
        result = self.ocr.ocr(img_path, cls=True)
        text_data = []
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                text_data.append(line[1][0])
        return '\n'.join(text_data)

    def save_text_to_file(self, text, file_path):
        with open(file_path, 'w') as f:
            f.write(text)

# Usage example:
if __name__ == "__main__":
    ocr_processor = TextExtractor(lang='en', use_gpu=False)
    img_path = '../pages/bigstructureimg.png'
    formatted_text = ocr_processor.extract_text(img_path)
    ocr_processor.save_text_to_file(formatted_text, 'formatted_text_data_2.txt')
