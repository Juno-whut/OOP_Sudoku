import random
import numpy as np
from copy import *

BOARD_SIZE = 9
BOX_SIZE = int(np.sqrt(BOARD_SIZE))
class Board: 
    """
    A class representing a Sudoku board.
    
    Attributes
    ----------
    grid: list of list of int
        The 9x9 grid representing the Sudoku board.
    
    difficulty_values: dict
        A dictionary mapping difficulty level to the number of empty cells to be created. 
    
    Methods
    -------
    __init__(self,difficulty="easy"):
        Initializes the Sudoku board with the given difficulty level.
    
    __create_board(self, difficulty: str="easy"):
        Creates a new Sudoku board of a given difficulty level.
    
    is_solved(self) -> bool:
        Checks wether the Sudoku board is solved or not.
    
    get_grid(self) -> list of list of int:
        Returns current state of Sudoku board.
    
    get_valid_numbers(self, row, col) -> list of int:
        Returns a list of valid numbers that can be placed in a given cell.
    
    get_empty_cells(self) -> list of tuple of int:
        Returns a list of empty cells in the Sudoku board.
    
    get_row(self, row) -> list of int:
        Returns row with given index in the Sudoku board.

    get_col(self, col) -> list of int:
        Returns column with given index in the Sudoku board.

    get_box(self, row, col) -> list of int:
        Returns the 3x3 box that contains the cell with the given row and column index.
    
    get_min_remaining_values_cell(self) -> tuple of int or None:
        Returns the cell with the least number of valid numbers that can be placed in it.
    
    solve(self) -> bool:
        Solves the Sudoku board using backtracking and returns True if succesful, False otherwise.
    
    print_board(self):
        Prints the Sudoku board in a readable format.
    """ 
    difficulty_values = {
        "easy": 30,
        "medium": 40,
        "hard": 50,
        "expert": 60,
    }
    
    def __init__(self, difficulty="easy"):
        """
        Initializes a new instance of the Board class.

        Args:
        - difficulty (str): A string representing the difficulty level of the Sudoku puzzle. 
          It must be one of the following: "easy", "medium", "hard", "expert". 
          Default is "easy".
        """
        assert difficulty != self.difficulty_values, f"{difficulty} is not a valid difficulty, Please enter a difficulty: easy, medium, hard, or expert"

        self.__create_board(difficulty)
    
    def __create_board(self, difficulty: str = "easy"):
        """
        Generates a new Sudoku board with the specified difficulty level.

        Args:
        - difficulty (str): A string representing the difficulty level of the Sudoku puzzle. 
          It must be one of the following: "easy", "medium", "hard", "expert". 
          Default is "easy".
        """        
        self.grid = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.solve()

        num_zeros = self.difficulty_values[difficulty]
        cells = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)]
        random.shuffle(cells)
        for i, j in cells:
            temp = self.grid[i][j]
            self.grid[i][j] = 0
            count = 0
            for _ in range(10):
                temp_board = deepcopy(self)
                temp_board.grid[i][j] = temp
                temp_board.solve()
                if temp_board.is_solved():
                    count += 1
                if count > 1:
                    self.grid[i][j] = temp
                    break
            if len(self.get_empty_cells()) >= num_zeros:
                break

    def is_solved(self):
        """
        Returns a boolean value indicating wether the Sudoku board is solved or not
        """
        return not self.get_empty_cells() and all(self.get_valid_numbers(i, j) == [self.grid[i][j]] for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)) 
           
    def get_grid(self):
        """
        Returns the current state of the Sudoku board.
        """
        return deepcopy(self.grid)
   
    
    
    def get_valid_numbers(self, row, col):
        """
        Returns a list of valid numbers that can be placed in the specified cell of the Sudoku board.

        Args:
        - row (int): The row index of the cell.
        - col (int): The column index of the cell.
        """
        used_nums = set(self.get_row(row) + self.get_col(col) + self.get_box(row, col))
        return [num for num in range(1, 10) if num not in used_nums]
    
    def get_empty_cells(self):   
        """
        Returns a list of all the empty cells (cells with the value 0) in the Sudoku board.
        """
        return list(zip(*np.where(np.array(self.grid) == 0 )))

    def get_row(self, row):
        """
        Returns a list of numbers in the specified row of the Sudoku board.

        Args:
        - row (int): The index of the row.
        """
        return self.grid[row]
        
    def get_col(self, col):
        """
        Returns a list of numbers in the specified column of the Sudoku board.

        Args:
        - col (int): The index of the column.
        """
        return [self.grid[i][col] for i in range(BOARD_SIZE)]

    def get_box(self, row, col):
        """
        Returns a list of value in the 3x3 box containg the cell at row, col.

        Args:
        row (int): Row index of the cell.
        col (int): Column index of the cell.

        Returns:
        list: A list of the 9 values in the box containing the cell.
        """

        box_row = (row // BOX_SIZE) * BOX_SIZE
        box_col = (col // BOX_SIZE) * BOX_SIZE
        return [self.grid[box_row + i][box_col + j] for i in range(BOX_SIZE) for j in range(BOX_SIZE)]
    
    def get_min_remaining_values_cell(self):
        """
        Returns the empty cell with the minimum number of possible valid values.

        Returns:
        tuple: A tuple representing the (row, column) indices of the empty cell with minimum possible valid values, or None if no empty cells exist.
        """
        empty_cells = self.get_empty_cells()
        if not empty_cells:
            return None
        return min(empty_cells, key=lambda x: len(self.get_valid_numbers(*x)))

    def solve(self):
        """
        Recursively solves the Sudoku board using backtracking.

        Returns:
            bool: True if the board was solved, False otherwise.
        """
        cell = self.get_min_remaining_values_cell()
        if not cell:
            return True

        row, col = cell
        valid_nums = self.get_valid_numbers(row, col)
        for num in valid_nums:
                self.grid[row][col] = num
                if self.solve():
                    return True
                self.grid[row][col] = 0

        return False

    def print_board(self):
        """
        Prints the current Sudoku board to the console in a reable format.
        """
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                print(self.grid[i][j], end=" ")
                if (j + 1) % BOX_SIZE == 0 and j != 8:
                    print("|", end=" ")
            print()
            if (i + 1) % BOX_SIZE == 0 and i != 8:
                print("- - - - - - - - - - - ")

    
if __name__ == '__main__':
    
    board = Board(difficulty="expert")

    board.print_board()
    board.solve()
    print("======================")
    board.print_board()
    