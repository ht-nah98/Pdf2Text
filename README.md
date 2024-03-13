# Image to Text Converter

This Python script `main.py` converts images containing textual and tabular data into text files, using OCR (Optical Character Recognition) and table extraction techniques.

## Usage

1. **Installation**:

   - Install the required dependencies by running:
     ```
     pip install -r requirements.txt
     ```

2. **Running the Script**:

   - Replace `img_path` variable with the path to the image you want to process.
   - Run the script using:
     ```
     python main.py
     ```

3. **Output**:

   - The script processes the image and generates a text file (`output.txt`) containing the extracted text and table data.

## Dependencies

- PIL (Python Imaging Library)
- NumPy
- pdf2image
- tqdm
- codes (Custom modules)
  - `tableFigureConverter`: Module containing the `TableFigureExtractor` class for extracting text and tables from images.
  - `structureWith3column`: Module containing the `PdfProcessor` class for processing PDF structures.

## Additional Notes

- The script utilizes OCR techniques to extract text from images.
- Tables and figures detected in the image are processed separately using the `TableFigureExtractor` class.
- Adjustments can be made to the `PdfProcessor` class depending on the structure of the PDF.

## File Structure

- `main.py`: The main script for image processing.
- `requirements.txt`: List of Python dependencies required to run the script.
- `codes/`: Directory containing custom modules for text and table extraction.

# Image to Word Converter

This Python script (`main.py`) converts images to words and saves the output to a text file.

## Usage

1. **Select Processor**: Choose a suitable processor for the layout of your image. Depending on the structure (e.g., number of columns), you may need to change the processor. For example:

   ```python
   # from codes.structureWith1Column import PdfProcessor
   # from codes.structureWith2Column import PdfProcessor
   from codes.structureWith3column import PdfProcessor
   processor = PdfProcessor()  # Change the processor based on image layout (e.g., 1, 2, or 3 columns)


# Table and Figure Extractor

This Python class `TableFigureExtractor` provides functionality to extract text from images, detect table and figure boundaries, and fill a grid structure with the extracted text.

## Features

- **Text Extraction**: Utilizes PaddleOCR for extracting text from images.
- **Box Detection**: Detects horizontal and vertical boxes based on bounding box coordinates.
- **Non-Maximum Suppression**: Performs non-maximum suppression to filter out overlapping boxes.
- **Grid Structure Filling**: Fills a grid structure with text based on detected boxes and texts.

## Usage

1. **Initialization**:

   ```python
   from TableFigureExtractor import TableFigureExtractor

   # Initialize with an image or region
   extractor = TableFigureExtractor(img_or_region, lang='en', use_gpu=False)

# Find Number of Columns

This Python script `findNumberOfColumns.py` is used to determine the number of columns in an image based on the positions of bounding boxes.

## Usage

1. **Running the Script**:

   - Ensure you have Python installed on your system.
   - Install the required dependencies using pip:
     ```
     pip install opencv-python
     ```
   - Run the script using:
     ```
     python findNumberOfColumns.py
     ```

2. **Functionality**:

   - The script takes a list of bounding boxes and the width of the image as input.
   - It calculates the central points of each bounding box and sorts them based on the x-coordinate.
   - By dividing the image width into three equal parts, it determines the column boundaries.
   - It then counts the number of points falling into each column.
   - Finally, based on the counts, it determines the number of columns present in the image.

## Function Explanation

The `determine_number_of_columns` function in the script determines the number of columns based on the positions of bounding boxes. It takes the following arguments:

- `bboxes (list)`: List of bounding boxes with format [x_min, y_min, x_max, y_max].
- `image_width (int)`: Width of the image.

The function returns an integer representing the number of columns detected.

# Layer Detection

The `layoutDetection.py` script is used to detect the layout and structure of PNG images, visualize the detected structure on the image, and save the resulting structure data.

## Usage

1. **Installation**:

   - Ensure you have Python installed on your system.
   - Install the required dependencies using pip:
     ```
     pip install paddleocr opencv-python pillow
     ```

2. **Running the Script**:

   - Modify the `img_path` variable to point to the PNG image file you want to analyze.
   - Run the script using:
     ```
     python layer_detection.py
     ```

3. **Functionality**:

   - The script utilizes the PaddleOCR library for detecting the structure of PNG images.
   - It loads the image specified by `img_path`.
   - It processes the image to detect its structure and layout using PPStructure from PaddleOCR.
   - The detected structure is saved in a folder specified by `save_folder` with the same name as the input image.
   - The script also visualizes the detected structure on the original image and saves the result as a JPEG image in the `save_directory`.

## Code Explanation

- The script initializes a PPStructure object with table and OCR detection disabled (`table=False, ocr=False`).
- To getting fulldata with full information with each block we need to change into (`recovery=True, use_gpu=False`)
- It reads the input PNG image using OpenCV (`cv2.imread()`).
- The detected structure is saved using `save_structure_res()` from PaddleOCR.
- The script then sorts the result based on the position of the bounding boxes.
- It visualizes the detected structure on the original image using `draw_structure_result()`.
- Finally, it saves the resulting image with the detected structure using Pillow (`Image.save()`).


