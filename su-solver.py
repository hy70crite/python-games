# using dancing link algorithm


class DLXNode:
    def __init__(self):
        self.left = self.right = self.up = self.down = self
        self.column = None

class DLXColumn:
    def __init__(self):
        self.header = DLXNode()
        self.size = 0

class SudokuSolver:
    def __init__(self, board):
        self.board = board
        self.root = DLXNode()
        self.columns = [DLXColumn() for _ in range(324)]
        self.nodes = []
        self.create_nodes()

    def create_nodes(self):
        for i in range(9):
            for j in range(9):
                for k in range(9):
                    node = DLXNode()
                    node.column = self.columns[i*27 + j*9 + k]
                    node.column.size += 1
                    self.nodes.append(node)
                    self.root.right.left = node
                    node.right = self.root
                    self.root.left.right = node
                    node.left = self.root

    def cover(self, column):
        column.header.right.left = column.header.left
        column.header.left.right = column.header.right
        i = column.header.down
        while i != column.header:
            j = i.right
            while j != i:
                j.column.size -= 1
                j.down.up = j.up
                j.up.down = j.down
                j = j.right
            i = i.down

    def uncover(self, column):
        i = column.header.up
        while i != column.header:
            j = i.left
            while j != i:
                j.column.size += 1
                j.down.up = j
                j.up.down = j
                j = j.left
            i = i.up
        column.header.right.left = column.header
        column.header.left.right = column.header

    def search(self, k):
        if self.root.right == self.root:
            return True
        s = min((c.size, c) for c in self.columns if c.size > 0)[1]
        self.cover(s)
        r = s.header.down
        while r != s.header:
            j = r.right
            while j != r:
                if j.column.size > 0:
                    self.cover(j.column)
                    if self.search(k + 1):
                        return True
                    self.uncover(j.column)
                j = j.right
            r = r.down
        self.uncover(s)
        return False

    def solve(self):
        if self.search(0):
            for i in range(9):
                for j in range(9):
                    for k in range(9):
                        node = self.nodes[i*81 + j*9 + k]
                        if node.column.size == 1:
                            self.board[i][j] = k + 1
                            break
            return True
        return False

def print_board(board):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")

def input_board():
    board = []
    for i in range(9):
        row = input("Enter row {} (separate numbers with spaces): ".format(i+1))
        row = list(map(int, row.split()))
        board.append(row)
    return board

def main():
    print("Welcome to the Sudoku Solver!")
    print("Please enter a Sudoku puzzle, one row at a time.")
    print("Use 0 to represent empty cells.")
    board = input_board()
    solver = SudokuSolver(board)
    if solver.solve():
        print("Solution:")
        print_board(board)
    else:
        print("No solution exists")

if __name__ == "__main__":
    main()

