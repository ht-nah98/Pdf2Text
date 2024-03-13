# Image to Word Converter

This Python script (`main.py`) converts images to words and saves the output to a text file.

## Usage

1. **Select Processor**: Choose a suitable processor for the layout of your image. Depending on the structure (e.g., number of columns), you may need to change the processor. For example:

   ```python
   processor = PdfProcessor()  # Change the processor based on image layout (e.g., 1, 2, or 3 columns)
2. Process Image Structure: Use the chosen processor to process the structure of the image. This step detects bounding boxes and extracts data from them. Example:
   ```python
   result_sorted = processor.process_structure(img_path).
3. Handle Table or Figure Data: Import the TableFigureExtractor class to handle table or figure data when converting them into the word text file.
   ```python
   from TableFigureExtractor import TableFigureExtractor
 
