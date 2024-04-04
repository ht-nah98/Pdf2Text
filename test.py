# def cell_symbol_at_time_recursive(N, K):
#     total_cells = 2 ** (N - 1)
#     if K < 1 or K > total_cells:
#         return None
#
#     if N == 1:
#         return 'X'
#
#     half = total_cells // 2
#     if K <= half:
#         return cell_symbol_at_time_recursive(N - 1, K)
#     else:
#         return 'Y' if cell_symbol_at_time_recursive(N - 1, K - half) == 'X' else 'X'
#
# def generate_symbol_array_recursive(pairs):
#     symbols = []
#     for N, K in pairs:
#         symbol = cell_symbol_at_time_recursive(N, K)
#         symbols.append(symbol)
#     return symbols
#
# # Example input as list of N, K pairs
# pairs = [(1, 1), (2, 2), (3, 4), (4,1), (4,6)]
#
# symbols = generate_symbol_array_recursive(pairs)
#
# for symbol in symbols:
#     print(symbol)

def process_input(input_lines):
    T = int(input_lines[0])
    pairs = [tuple(map(int, line.split())) for line in input_lines[1:T+1]]
    return T, pairs
def cell_symbol_at_time_recursive(N, K):
    total_cells = 2 ** (N - 1)
    if K < 1 or K > total_cells:
        return None

    if N == 1:
        return 'X'

    half = total_cells / 2
    if K <= half:
        return cell_symbol_at_time_recursive(N - 1, K)
    else:
        return 'Y' if cell_symbol_at_time_recursive(N - 1, K - half) == 'X' else 'X'


def generate_symbol_array_recursive(pairs):
    symbols = []
    for N, K in pairs:
        symbol = cell_symbol_at_time_recursive(N, K)
        symbols.append(symbol)
    return symbols


input_lines = [
    "3",
    "1 1",
    "2 2",
    "5 3",
    "9 9",
    "10 10"
]

T, pairs = process_input(input_lines)

symbols = generate_symbol_array_recursive(pairs)

for symbol in symbols:
    print(symbol)