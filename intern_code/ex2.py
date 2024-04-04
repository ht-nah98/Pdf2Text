def find_parent(parent, i):
    if parent[i] == i:
        return i
    return find_parent(parent, parent[i])

def union(parent, rank, x, y):
    x_root = find_parent(parent, x)
    y_root = find_parent(parent, y)

    if rank[x_root] < rank[y_root]:
        parent[x_root] = y_root
    elif rank[x_root] > rank[y_root]:
        parent[y_root] = x_root
    else:
        parent[y_root] = x_root
        rank[x_root] += 1

def minimum_changes(N, M, connections):
    if N >= 5 * (10**5) or M>= (10**6) or M >= (N * (N - 1)) / 2:
        return -1

    if M < N - 1:
        return -1

    parent = [i for i in range(N)]
    rank = [0] * N
    seen_connections = set()

    for u, v in connections:
        if (u, v) in seen_connections or (v, u) in seen_connections:
            return -1
        if not (0 <= u <= N - 1 and 0 <= v <= N - 1):
            return -1
        seen_connections.add((u, v))
        union(parent, rank, u, v)

    components = set()
    for i in range(N):
        components.add(find_parent(parent, i))

    if len(components) > 1:
        return M - (N - 1) + len(components) - 1

    return M - (N - 1)

# Example usage:
N = 7
M = 6
connections = [(0, 1), (0, 2), (6, 3), (3, 1), (2, 3), (2, 1)]

print(minimum_changes(N, M, connections))
