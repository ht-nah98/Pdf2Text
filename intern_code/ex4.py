
def solve_addition_problems(problems):
    solutions = []
    for problem in problems:
        solution = sum(problem)
        solutions.append(solution)
    return solutions


N = int(input())
problems = []
for _ in range(N):
    a, b = map(int, input().split())
    problems.append((a, b))


solutions = solve_addition_problems(problems)


for solution in solutions:
    print(solution)
