import random
from enum import Enum


class Cell(Enum):
    """The cell type of the maze.
    
    A class for managing numbers stored in an array.

    Attributes:
        ROAD (int):road in the maze.
        WALL (int):wall in the maze.
        ENTRY (int):entry point in the maze.
        EXIT (int):exit point in the maze.
        FOURTY_TWO (int):42 point in the maze.
    """
    ROAD = 0
    WALL = 1
    ENTRY = 2
    EXIT = 3
    FOURTY_TWO = 4


class MazeGenerator:
    """A class for generating a maze.
    
    Attributes:
        width (int):width of the maze.
        height (int):height of the maze.
        entry_point (tuple[int, int]):entry point of the maze.
        exit_point (tuple[int, int]):exit point of the maze.
        seed (int | None):seed for random number generation.
        grid (list[list[int]]):grid of the maze.
    """
    def __init__(self, width: int, height: int, entry_point: tuple[int, int],
            exit_point: tuple[int, int], seed: int | None = None) -> None:
        """Initialize the MazeGenerator.

        Args:
            width (int):Number of cells in the width of the maze.
            height (int):Number of cells in the height of the maze.
            entry_point (tuple[int, int]):entry point of the maze.
            exit_point (tuple[int, int]):exit point of the maze.
            seed (int | None):seed for random number generation.
        """
        self.width = width
        self.height = height
        self.entry_point = entry_point
        self.exit_point = exit_point
        self.seed = seed
        
        # 横と縦の配列の長さ
        self.w_grid = width * 2 + 1
        self.h_grid = height * 2 + 1

        # 横の配列を内包した縦の配列のリスト
        self.grid: list[list[int]] = [
            [Cell.ROAD.value for _ in range(self.w_grid)]
            for _ in range(self.h_grid)
        ]

    def generate(self) -> None:
        """Generate a maze."""
        if self.seed is not None:
            random.seed(self.seed)
        self._build_outer_walls()
        self._place_pillars_and_knock_down()

        ex, ey = self.entry_point
        self.grid[ey * 2 + 1][ex * 2 + 1] = Cell.ENTRY.value

        gx, gy = self.exit_point
        self.grid[gy * 2 + 1][gx * 2 + 1] = Cell.EXIT.value
        
        if self.width >= 7 and self.height >= 5:
            self._build_fourty_two()

    def _build_outer_walls(self) -> None:
        """
        Build outer walls of the maze.
        """
        for y in range(0, self.h_grid):
            for x in range(0, self.w_grid):
                if y == 0 or x == 0 or y == self.h_grid - 1 or x == self.w_grid - 1:
                    self.grid[y][x] = Cell.WALL.value

    def _build_fourty_two(self) -> None:
        """
        Build the number 42 in the maze.
        """
        self.grid[self.height//2][2] = Cell.FOURTY_TWO.value
        self.grid[2][3] = Cell.FOURTY_TWO.value
        self.grid[2][4] = Cell.FOURTY_TWO.value
        self.grid[3][2] = Cell.FOURTY_TWO.value
        self.grid[3][4] = Cell.FOURTY_TWO.value
        self.grid[4][2] = Cell.FOURTY_TWO.value
        self.grid[4][3] = Cell.FOURTY_TWO.value
        self.grid[4][4] = Cell.FOURTY_TWO.value

    def _place_pillars_and_knock_down(self) -> None:
        """
        Place pillars and knock down walls.
        """
        for y in range(2, self.h_grid - 1, 2):
            for x in range(2, self.w_grid - 1, 2):
                self.grid[y][x] = Cell.WALL.value
                if y == 2 and x == 2: # 一番上の一番左は左下右上(WSEN)
                    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
                elif y == 2: # 一番上のそれ以外は下右上(SEN)
                    directions = [(0, 1), (1, 0), (0, -1)]
                elif x == 2: #一番左(上記を除く)は左下右(WSE)
                    directions = [(-1, 0), (0, 1), (1, 0)]
                else: # 上から二番目、左から二番目は下右(SE)
                    directions = [(0, 1), (1, 0)]

                dx, dy = random.choice(directions)
                self.grid[y + dy][x + dx] = Cell.WALL.value


    def get_grid(self) -> list[list[int]]:
        """
        Get the grid of the maze.
        """
        return self.grid

