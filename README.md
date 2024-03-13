e# Image to Word Converter

This Python script (`main.py`) converts images to words and saves the output to a text file.

## Usage

1. **Select Processor**: Choose a suitable processor for the layout of your image. Depending on the structure (e.g., number of columns), you may need to change the processor. For example:

   ```python
   processor = PdfProcessor()  # Change the processor based on image layout (e.g., 1, 2, or 3 columns)
2. Process Image Structure: Use the chosen processor to process the structure of the image. This step detects bounding boxes and extracts data from them. Example:
   result_sorted = processor.process_structure(img_path).
3. Handle Table or Figure Data: Import the TableFigureExtractor class to handle table or figure data when converting them into the word text file.
   from TableFigureExtractor import TableFigureExtractor

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

 
