from itertools import combinations
from solvers.simple_backtracking import check


def calculate_domains(y_nums, x_nums):
    width = len(x_nums)
    height = len(y_nums)
    valid_cols = [[] for i in range(width)]
    valid_rows = [[] for i in range(height)]

    for i in range(width):
        n_groups = len(x_nums[i])
        n_empty = min(height, height - (n_groups - 1) - sum(x_nums[i]))
        comb = list(combinations(range(n_groups + n_empty), n_groups))
        for group_loc in comb:
            column = []
            group_id = 0
            for j in range(n_groups + n_empty):
                if j in group_loc:
                    column += [1] * x_nums[i][group_id]
                    group_id += 1
                    if group_id != n_groups:
                        column += [2]
                else:
                    column += [2]
            valid_cols[i].append(column)

    for i in range(height):
        n_groups = len(y_nums[i])
        n_empty = min(width, width - (n_groups - 1) - sum(y_nums[i]))
        comb = list(combinations(range(n_groups + n_empty), n_groups))
        for group_loc in comb:
            row = []
            group_id = 0
            for j in range(n_groups + n_empty):
                if j in group_loc:
                    row += [1] * y_nums[i][group_id]
                    group_id += 1
                    if group_id != n_groups:
                        row += [2]
                else:
                    row += [2]
            valid_rows[i].append(row)

    return valid_cols, valid_rows


def update_cols(valid_cols, row, idx):
    width = len(row)
    new_cols = [[] for i in range(width)]
    for i in range(width):
        for c in valid_cols[i]:
            if c[idx] == row[i]:
                new_cols[i].append(c)
    return new_cols


def update_rows(valid_rows, col, idx):
    height = len(col)
    new_rows = [[] for i in range(height)]
    for i in range(height):
        for r in valid_rows[i]:
            if r[idx] == col[i]:
                new_rows[i].append(r)
    return new_rows


def find_min_unfixed(valid_cols, valid_rows, fixed_cols, fixed_rows):
    min_rem_col = -1
    for i in range(len(valid_cols)):
        if (min_rem_col == -1 or len(valid_cols[i]) < len(valid_cols[min_rem_col])) and not fixed_cols[i]:
            min_rem_col = i

    min_rem_row = -1
    for i in range(len(valid_rows)):
        if (min_rem_row == -1 or len(valid_rows[i]) < len(valid_rows[min_rem_row])) and not fixed_rows[i]:
            min_rem_row = i

    return min_rem_col, min_rem_row


def recur_solve(y_nums, x_nums, valid_cols, valid_rows, fixed_cols, fixed_rows):
    width = len(x_nums)
    height = len(y_nums)

    min_rem_col, min_rem_row = find_min_unfixed(valid_cols, valid_rows, fixed_cols, fixed_rows)

    if min(len(valid_cols[min_rem_col]), len(valid_rows[min_rem_row])) == 0:
        raise IndexError

    if len(max(valid_cols, key=len)) == 1:
        assignment = [[0] * width for i in range(height)]
        for i in range(height):
            for j in range(width):
                assignment[i][j] = valid_cols[j][0][i]
        if check(y_nums, x_nums, assignment):
            return assignment

    if len(max(valid_rows, key=len)) == 1:
        assignment = [[0] * width for i in range(height)]
        for i in range(height):
            for j in range(width):
                assignment[i][j] = valid_rows[i][0][j]
        if check(y_nums, x_nums, assignment):
            return assignment

    if len(valid_cols[min_rem_col]) < len(valid_rows[min_rem_row]):
        for i in range(len(valid_cols[min_rem_col])):
            col = valid_cols[min_rem_col][i]
            new_cols = valid_cols[:min_rem_col] + [[col]] + valid_cols[min_rem_col + 1:]
            new_fixed_cols = fixed_cols[:min_rem_col] + [1] + fixed_cols[min_rem_col + 1:]
            new_rows = update_rows(valid_rows, col, min_rem_col)
            ans = recur_solve(y_nums, x_nums, new_cols, new_rows, new_fixed_cols, fixed_rows)
            if ans is not None:
                return ans
    else:
        for i in range(len(valid_rows[min_rem_row])):
            row = valid_rows[min_rem_row][i]
            new_rows = valid_rows[:min_rem_row] + [[row]] + valid_rows[min_rem_row + 1:]
            new_fixed_rows = fixed_rows[:min_rem_row] + [1] + fixed_rows[min_rem_row + 1:]
            new_cols = update_cols(valid_cols, row, min_rem_row)
            ans = recur_solve(y_nums, x_nums, new_cols, new_rows, fixed_cols, new_fixed_rows)
            if ans is not None:
                return ans


def solve(y_nums, x_nums):
    valid_cols, valid_rows = calculate_domains(y_nums, x_nums)
    fixed_cols = [0] * len(x_nums)
    fixed_rows = [0] * len(y_nums)
    return recur_solve(y_nums, x_nums, valid_cols, valid_rows, fixed_cols, fixed_rows), False


# Convert grid object attributes to correct form for solving.
def solve_grid(width, height, x_nums, y_nums):
    ans = solve(y_nums, x_nums)
    return ans