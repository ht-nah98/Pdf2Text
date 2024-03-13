
from PIL import Image
import numpy as np
from pdf2image import convert_from_path
import tqdm
import os
from codes.tableFigureConverter import TableFigureExtractor
from codes.structureWith1Column import PdfProcessor
# from codes.structureWith2Column import PdfProcessor
# from codes.structureWith3Column import PdfProcessor


def process_result_sorted(result_sorted, img_path, output_dir):
    def process_region(img, bbox, file):
        region = img.crop(bbox)
        region_np = np.array(region.convert("RGB"))
        table_extractor = TableFigureExtractor(region_np, lang='en', use_gpu=False)
        table_extractor.img_or_region = region_np
        boxes, probs, texts = table_extractor.extract_text()
        image_height, image_width, _ = region_np.shape
        horiz_box, verti_box = table_extractor.detect_boxes(boxes, image_width, image_height)
        horiz_lines = table_extractor.perform_non_max_suppression(np.array(horiz_box), np.array(probs))
        verti_lines = table_extractor.perform_non_max_suppression(np.array(verti_box), np.array(probs))
        out_array = table_extractor.fill_grid_structure(horiz_lines, verti_lines, boxes, texts, verti_box, horiz_box)
        table_extractor.write_to_txt(out_array, file, separator='|')
        file.write('\n')  # Add a newline character to insert a break

    img_name = os.path.splitext(os.path.basename(img_path))[0]
    output_file_path = os.path.join(output_dir, f"{img_name}.txt")

    with open(output_file_path, "a", encoding="utf-8") as file:
        for line in result_sorted:
            if line['type'] == 'text' or line['type'] == 'reference' or line['type'] == 'title' or line['type'] == 'footer' or line['type'] == 'figure_caption':
                if isinstance(line['res'], list):
                    text_lines = [res['text'] for res in line['res']]
                    text = ' '.join(text_lines)
                    file.write(text + "\n")
                else:
                    file.write(line['res'] + "\n")
            elif line['type'] == 'table':
                table_regions = [line['bbox']]
                img = Image.open(img_path)
                for bbox in table_regions:
                    process_region(img, bbox, file)
            elif line['type'] == 'figure':
                if line['res']:
                    figure_regions = [line['bbox']]
                    img = Image.open(img_path)
                    for bbox in figure_regions:
                        process_region(img, bbox, file)
                else:
                    file.write("\n")
            else:
                file.write("\n")


def process_images_in_directory(directory_path, output_dir):
    processor = PdfProcessor()
    for filename in os.listdir(directory_path):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            img_path = os.path.join(directory_path, filename)
            result_sorted = processor.process_structure(img_path)
            process_result_sorted(result_sorted, img_path, output_dir)


# Directory containing the images
img_directory = './imgTestv1/imgTables'
output_directory = './imgTestv1/imgTables'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Process all images in the directory
process_images_in_directory(img_directory, output_directory)






