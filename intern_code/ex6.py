# MOD = 10 ** 9 + 7
# x = 207617170
# def count_ways(n):
#     # The number of rows in the table is the number of positions (n)
#     # and the number of columns is the number of tree types (5).
#
#     dp = [[0] * 5 for _ in range(n)]
#     for i in range(5):
#         dp[0][i] = 1
#
#     # A = Hồng, B = Ly, C = Mai, D = Lan, E = Tulip
#     for i in range(1, n):
#         dp[i][0] = dp[i - 1][1]  # Plant A can only be planted after Plants B
#         dp[i][1] = dp[i - 1][0] + dp[i - 1][2]  # Plant B can only be planted after plant A or plant C
#         dp[i][2] = dp[i - 1][0] + dp[i - 1][1] + dp[i - 1][3] + dp[i - 1][4]  # There are no two consecutive C Plants
#         dp[i][3] = dp[i - 1][2] + dp[i - 1][4]  # Plant D can only be planted after plant C or plant E
#         dp[i][4] = dp[i - 1][0]  # Plant E can only be planted after plant A
#
#     total_ways = sum(dp[-1]) % MOD
#
#     return total_ways
#
# N = 100000
# print(count_ways(N))


MOD = 10 ** 9 + 7
x = 207617170
def count_ways(n):
    # The number of rows in the table is the number of positions (n)
    # and the number of columns is the number of tree types (5).

    prev = [1] * 5

    # A = Hồng, B = Ly, C = Mai, D = Lan, E = Tulip
    for i in range(1, n):
        curr = [0] * 5
        curr[0] = prev[1]  # Plant A can only be planted after Plants B
        curr[1] = prev[0] + prev[2]  # Plant B can only be planted after plant A or plant C
        curr[2] = prev[0] + prev[1] + prev[3] + prev[4]  # There are no two consecutive C Plants
        curr[3] = prev[2] + prev[4]  # Plant D can only be planted after plant C or plant E
        curr[4] = prev[0]  # Plant E can only be planted after plant A
        prev = curr

    total_ways = sum(prev) % MOD

    return total_ways

N = 1000000
print(count_ways(N))
