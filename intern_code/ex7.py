def max_sum_with_condition(N, K):
    if K >= len(N):
        return sum(N)

    # Tính tổng tối đa từ đầu đến index K
    max_sum = sum(N[:K])
    current_sum = max_sum

    # Dùng sliding window để tính tổng tối đa không có 4 số liên tiếp
    for i in range(K, len(N)):
        # Trừ đi phần tử đầu tiên của cửa sổ trượt
        current_sum -= N[i - K]
        # Thêm phần tử mới của cửa sổ trượt
        current_sum += N[i]
        # Cập nhật tổng tối đa nếu cần
        max_sum = max(max_sum, current_sum)

    return max_sum


# Dãy số N và số K
N = [8, 6, 2, 5, 7, 10, 5, 7, 6, 3]
K = 3

# In ra tổng giá trị lớn nhất thoả mãn điều kiện
print("Tổng giá trị lớn nhất:", max_sum_with_condition(N, K))
