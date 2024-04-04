import numpy as np


def find_projection_point(A, B, C):
    # Tính vector AB
    AB = B - A

    # Tính vector AC
    AC = C - A

    # Tính độ dài của vector AB
    AB_length = np.linalg.norm(AB)

    # Tính phép chiếu của vector AC lên AB
    projection_length = np.dot(AC, AB) / AB_length

    # Tính toạ độ của điểm H trên đường thẳng AB
    H = A + (projection_length / AB_length) * AB

    return H


# Tính độ dài các đoạn thẳng
def calculate_lengths(A, B, H):
    AH_length = np.linalg.norm(H - A)
    BH_length = np.linalg.norm(H - B)
    AB_length = np.linalg.norm(B - A)

    return AH_length, BH_length, AB_length


# So sánh vị trí của H so với AB
def compare_positions(AH_length, BH_length, AB_length):
    if AH_length > AB_length or BH_length > AB_length:
        return "H nằm ngoài đoạn AB"
    else:
        return "H nằm trên đoạn AB"


# Tìm vị trí tương đối của điểm C so với đoạn AB
def find_relative_position(A, B, C):
    # Tính vector AB và AC
    AB = B - A
    AC = C - A

    # Tính tích vô hướng của AB và AC để xác định vị trí của C so với đoạn AB
    cross_product = np.cross(AB, AC)

    if cross_product > 0:
        return "C nằm bên trái của đoạn AB"
    elif cross_product < 0:
        return "C nằm bên phải của đoạn AB"
    else:
        return "C nằm trên đường thẳng AB"


# Toạ độ điểm A và B
A = np.array([2, 0])
B = np.array([-3, 0])

# Toạ độ điểm C (bất kỳ)
C = np.array([4, -3])

# Tìm toạ độ điểm H
H = find_projection_point(A, B, C)

# Tính độ dài các đoạn thẳng
AH_length, BH_length, AB_length = calculate_lengths(A, B, H)

# So sánh vị trí của H so với AB
position = compare_positions(AH_length, BH_length, AB_length)

# Tìm vị trí tương đối của điểm C so với đoạn AB
relative_position = find_relative_position(A, B, C)

# In ra toàn bộ thông tin
print("Toạ độ của điểm H:", H)
print("Độ dài AH:", AH_length)
print("Độ dài BH:", BH_length)
print("Độ dài AB:", AB_length)
print(position)

# In ra thông điệp tương ứng với vị trí của H so với đoạn AB
if position == "H nằm ngoài đoạn AB":
    print("Điểm C nằm bên ngoài mặt phẳng P")
elif position == "H nằm trên đoạn AB":
    print("Điểm", relative_position)
