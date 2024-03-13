import cv2

def determine_number_of_columns(bboxes, image_width):
    """
    Determine the number of columns based on the positions of bounding boxes.

    Args:
        bboxes (list): List of bounding boxes with format [x_min, y_min, x_max, y_max].
        image_width (int): Width of the image.

    Returns:
        int: Number of columns detected.
    """
    # Calculate central points of each bounding box
    # Calculate central points of each bounding box
    central_points = [((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2) for bbox in bboxes]

    # Sort central points based on x-coordinate
    sorted_central_points = sorted(central_points)

    # Define column boundaries
    column_width = image_width / 3
    left_column_boundary = column_width
    right_column_boundary = column_width * 2

    # Initialize counters for points in each column
    left_count = 0
    middle_count = 0
    right_count = 0

    # Count points in each column
    for point in sorted_central_points:
        print(point)
        print(left_column_boundary)
        print(right_column_boundary)
        if point[0] < left_column_boundary:
            left_count += 1
        elif point[0] >= right_column_boundary:
            right_count += 1
        else:
            middle_count += 1
    print(left_count)
    print(right_count)
    print(middle_count)
    # Determine the number of columns based on the counts
    if left_count > 0 and middle_count > 0 and right_count > 0:
        return 3
    elif middle_count > 0:
        return 1
    else:
        return 2

# Example usage:
bboxes = [
    [41, 40, 241, 910],
    [269, 444, 455, 508],
    [495, 446, 682, 908],
    [495, 448, 683, 907],
    [270, 513, 462, 907],
]
img_path = '../pages/test1columns.png'
img = cv2.imread(img_path)
image_height, image_width, _ = img.shape


num_columns = determine_number_of_columns(bboxes, image_width)
print("Number of columns:", num_columns)