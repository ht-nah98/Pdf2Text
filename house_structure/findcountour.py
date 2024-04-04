import cv2
import numpy as np

def find_contours(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over the images in the input folder
    for filename in os.listdir(input_folder):
        # Read the input image
        image_path = os.path.join(input_folder, filename)
        image = cv2.imread(image_path)

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply adaptive thresholding to binarize the image
        binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 4)

        # Perform morphological operations to further clean up the binary image
        kernel = np.ones((5,5),np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        # Find contours in the binary image
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw the contours on a blank canvas
        contour_image = np.zeros_like(image)
        cv2.drawContours(contour_image, contours, -1, (255, 255, 255), 2)

        # Save the resulting contour image to the output folder
        output_path = os.path.join(output_folder, f'result_{filename}')
        cv2.imwrite(output_path, contour_image)

# Example usage:
input_folder = './madori'  # Input folder containing images
output_folder = './result_img'  # Output folder to save contour images
find_contours(input_folder, output_folder)