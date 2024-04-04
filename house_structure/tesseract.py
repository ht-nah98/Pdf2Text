import os
import cv2
import pytesseract

# Path to Tesseract executable (change this path according to your installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Set TESSDATA_PREFIX environment variable to the directory containing language data files
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'

# Read the input image
img_path = 'room2.jpg'
image = cv2.imread(img_path)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Use pytesseract to perform OCR on the grayscale image (specify language as 'jpn' or 'jpn_vert')
text = pytesseract.image_to_string(gray, lang='jpn')

# Print the extracted text
print("Extracted Text:")
print(text)
