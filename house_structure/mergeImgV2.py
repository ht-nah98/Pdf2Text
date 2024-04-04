# import os
# from PIL import Image
#
# def resize_and_concatenate_images(folder, merge_folder):
#     # Create merge folder if it doesn't exist
#     if not os.path.exists(merge_folder):
#         os.makedirs(merge_folder)
#
#     # Get list of files in the folder
#     files = os.listdir(folder)
#
#     # Filter files to select only the ones with "_close_wall" suffix
#     selected_files = [file for file in files if file.endswith("_close_wall.png")]
#
#     # Resize and concatenate images
#     for close_wall_file in selected_files:
#         # Extract the corresponding original image filename
#         original_file = close_wall_file.split("_close_wall")[0] + ".jpg"
#
#         # Check if the original image file exists
#         if original_file in files:
#             # Open and resize original image
#             original_path = os.path.join(folder, original_file)
#             original_img = Image.open(original_path)
#             original_img = original_img.resize((256, 256))
#
#             # Open and resize close wall image
#             close_wall_path = os.path.join(folder, close_wall_file)
#             close_wall_img = Image.open(close_wall_path)
#             close_wall_img = close_wall_img.resize((256, 256))
#
#             # Create a new image with width = 512 and height = 256
#             merged_img = Image.new('RGB', (512, 256))
#
#             # Paste original image on the left side
#             merged_img.paste(original_img, (0, 0))
#
#             # Paste close wall image on the right side
#             merged_img.paste(close_wall_img, (256, 0))
#
#             # Save the merged image
#             merged_img.save(os.path.join(merge_folder, f'merged_{original_file}'))
#
# # Example usage
# folder = './newyork/train'
# merge_folder = './newyork/train_merge'
#
# resize_and_concatenate_images(folder, merge_folder)


import os
from PIL import Image

def resize_and_concatenate_images(folder, merge_folder):
    # Create merge folder if it doesn't exist
    if not os.path.exists(merge_folder):
        os.makedirs(merge_folder)

    # Get list of files in the folder
    files = os.listdir(folder)

    # Filter files to select only the ones with "5_pre.jpg" and "_close_wall.png" filenames
    selected_files = [file for file in files if file.endswith("_pre.jpg")]

    # Resize and concatenate images
    for pre_file in selected_files:
        # Construct the corresponding close wall image filename
        close_wall_file = pre_file.replace("_pre.jpg", "_close_wall.png")

        # Check if the close wall image file exists
        if close_wall_file in files:
            # Open and resize pre image
            pre_path = os.path.join(folder, pre_file)
            pre_img = Image.open(pre_path)
            pre_img = pre_img.resize((256, 256))

            # Open and resize close wall image
            close_wall_path = os.path.join(folder, close_wall_file)
            close_wall_img = Image.open(close_wall_path)
            close_wall_img = close_wall_img.resize((256, 256))

            # Create a new image with width = 512 and height = 256
            merged_img = Image.new('RGB', (512, 256))

            # Paste pre image on the left side
            merged_img.paste(pre_img, (0, 0))

            # Paste close wall image on the right side
            merged_img.paste(close_wall_img, (256, 0))

            # Save the merged image
            merged_img.save(os.path.join(merge_folder, f'merged_{pre_file}'))

# Example usage
folder = './newyork/train'
merge_folder = './newyork/train_merge_preprocess'

resize_and_concatenate_images(folder, merge_folder)
