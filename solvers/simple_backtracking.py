def check(y_nums, x_nums, assignment):
    height = len(assignment)
    width = len(assignment[0])
    k = 0
    for i in range(height):
        block_pattern = []
        for j in range(width):
            if assignment[i][j] == 1:
                if j == 0:
                    block_pattern.append(1)
                else:
                    if assignment[i][j - 1] == 1:
                        block_pattern[-1] += 1
                    else:
                        block_pattern.append(1)
        if block_pattern != y_nums[i]:
            return False

    for j in range(width):
        block_pattern = []
        for i in range(height):
            if assignment[i][j] == 1:
                if i == 0:
                    block_pattern.append(1)
                else:
                    if assignment[i - 1][j] == 1:
                        block_pattern[-1] += 1
                    else:
                        block_pattern.append(1)
        if block_pattern != x_nums[j]:
            return False

    return True


def backtracking(y_nums, x_nums, assignment, unassigned):
    # Extremely slow due to being essentially unable to backtrack:
    # no easy way to check partial assignment validity
    if check(y_nums, x_nums, assignment):
        return assignment, False
    if len(unassigned) == 0:
        return None, None
    for i, j in unassigned:
        assignment[i][j] = 1
        unassigned.remove((i, j))
        res = backtracking(y_nums, x_nums, assignment, unassigned)
        if res[0] is not None:
            return res
        assignment[i][j] = 2
        res = backtracking(y_nums, x_nums, assignment, unassigned)
        if res[0] is not None:
            return res
        assignment[i][j] = 0
        unassigned.append((i, j))
    return None, None


# Convert grid object attributes to correct form for solving.
def solve_grid(width, height, x_nums, y_nums):
    grid = [[0]*width for i in range(height)]
    unassigned = []
    for i in range(height):
        for j in range(width):
            unassigned.append((i, j))
    ans = backtracking(y_nums, x_nums, grid, unassigned)
    return ans