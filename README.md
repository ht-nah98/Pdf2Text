main.py: use to convert from an img to word and save it to txt file.
	- processor = PdfProcessor(): we need to change the processor for different structure layout of png
	For example: with 1 or 2 or 3 columns. base on image we can choose suitable version of processor
	- result_sorted = processor.process_structure(img_path): result_sorted provied the data of bounding box we have detect with data inside
	- TableFigureExtractor: Import the main class to deal with table or figure data when we want to convert them into word.txt file
