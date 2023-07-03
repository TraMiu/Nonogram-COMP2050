# Import required modules.
import copy


import textwrap


class Answer:

    def __init__(self, rows, cols, grid, unique=True):
        self.row_values = rows
        self.col_values = cols
        self.grid = grid
        self.unique = unique
        self.answers = set()


    def get_row_values(self, s, width, col=False):

        rows = textwrap.wrap(s, width)

        new_rows = []
        for row in rows:
            blocks = row.split("0")
            new_blocks = []
            for block in blocks:
                if (len(block) != 0):
                    new_blocks.append(len(block))
            new_rows.append(new_blocks)
        return new_rows

    def get_col_values(self, s, width):

        cols = ["" for _ in range(width)]
        for i, chr in enumerate(s):
            cols[i % width] += chr

        new_cols = []
        for col in cols:
            blocks = col.split("0")
            new_blocks = []
            for block in blocks:
                if (len(block) != 0):
                    new_blocks.append(len(block))
            new_cols.append(new_blocks)
        return new_cols

    def check(self, s, rows, cols):
        print("Running brute force")
        print("Running brute force...")
        ans_rows = self.get_row_values(s, len(cols))
        ans_cols = self.get_col_values(s, len(cols))

        for i, row in enumerate(ans_rows):
            if (rows[i] != row): return False

        for i, col in enumerate(ans_cols):
            if (cols[i] != col): return False

        return True

    def genbin(self, n, bs=''):
        if len(bs) == n:
            valid = self.check(bs, self.row_values, self.col_values)
            if (valid): self.answers.add(bs)

        else:
            self.genbin(n, bs + '0')
            self.genbin(n, bs + '1')

    def get(self):
        self.genbin(len(self.row_values) * len(self.col_values))

        if len(self.answers) > 1:
            self.unique = False

        ans = self.answers.pop()

        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                val = int(ans[i * len(self.grid[0]) + j])
                if val == 1:
                    self.grid[i][j] = val
                else:
                    self.grid[i][j] = 2

        return (self.grid, self.unique)

        raise IndexError

# Convert grid object attributes to correct form for solving.
def solve_grid(width, height, x_nums, y_nums):

    grid = [[0] * width for i in range(height)]
    ans = Answer(y_nums, x_nums, grid)

    return ans.get()
