def convert_input_to_matrix(input_data):
    lines = input_data.split('\n')
    n, m = map(int, lines[0].split())
    matrix = []
    for line in lines[1:]:
        row = list(map(int, line.split()))
        matrix.append(row)
    return matrix


def maximalRectangle(matrix):
    if not matrix:
        return 0

    n, m = len(matrix), len(matrix[0])
    max_area = 0

    for i in range(n):
        for j in range(m):
            if matrix[i][j] == 1:
                width = 1
                while j + width < m and matrix[i][j + width] == 1:
                    width += 1

                height = 1
                while i + height < n:
                    valid = True
                    for k in range(j, j + width):
                        if matrix[i + height][k] != 1:
                            valid = False
                            break
                    if valid:
                        height += 1
                    else:
                        break
                # Check is rectangle contain all element 1 or not
                if all(matrix[i + r][j:j + width] == [1] * width for r in range(height)):
                    area = width * height
                    max_area = max(max_area, area)
    return max_area



def getValue(input_data):
    print(input_data)
    matrix = convert_input_to_matrix(input_data)
    print(maximalRectangle(matrix))

input_data = '''5 10
1 0 1 0 0 0 1 1 1 1
1 0 1 1 1 1 0 0 1 1
1 1 1 1 0 0 1 1 1 1
1 0 0 1 0 1 0 0 1 0
1 0 0 1 0 1 0 0 1 1'''
getValue(input_data)
