import os
from PIL import Image

def resize_and_concatenate_images(input_folder, result_folder, merge_folder):
    # Create merge folder if it doesn't exist
    if not os.path.exists(merge_folder):
        os.makedirs(merge_folder)

    # Get list of files in both wall and wall_close folders
    wall_files = os.listdir(input_folder)
    result_files = os.listdir(result_folder)
    # print(result_files)
    # Resize and concatenate images
    for wall_file in wall_files:
        # Remove the suffix from the mador filename
        mador_file_name = os.path.splitext(wall_file)[0]
        # print(mador_file_name)
        # Find corresponding madori_test_data file
        result_file = next((file for file in result_files if mador_file_name in file), None)
        # print(result_file)
        # If corresponding madori_test_data file exists
        if result_file:
            # Open and resize mador image
            mador_path = os.path.join(input_folder, wall_file)
            mador_img = Image.open(mador_path)
            mador_img = mador_img.resize((256, 256))

            # Open and resize madori_test_data image
            result_path = os.path.join(result_folder, result_file)
            result_img = Image.open(result_path)
            result_img = result_img.resize((256, 256))

            # Create a new image with width = 512 and height = 256
            merged_img = Image.new('RGB', (512, 256))

            # Paste mador image on the left side
            merged_img.paste(mador_img, (0, 0))

            # Paste madori_test_data image on the right side
            merged_img.paste(result_img, (256, 0))

            # Save the merged image
            merged_img.save(os.path.join(merge_folder, f'merged_{wall_file}'))

# Example usage
input_folder = './newyork/madori'
result_folder = './newyork/madori_test_data'
merge_folder = './newyork/mergeResult'

resize_and_concatenate_images(input_folder, result_folder, merge_folder)
