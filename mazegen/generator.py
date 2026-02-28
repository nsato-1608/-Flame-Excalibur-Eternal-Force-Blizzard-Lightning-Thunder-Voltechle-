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
    def __init__(self, width: int, height: int,
                 entry_point: tuple[int, int],
                 exit_point: tuple[int, int],
                 seed: int | None = None,
                 perfect: bool = False) -> None:
        """Initialize the MazeGenerator.

        Args:
            width (int):Number of cells in the width of the maze.
            height (int):Number of cells in the height of the maze.
            entry_point (tuple[int, int]):entry point of the maze.
            exit_point (tuple[int, int]):exit point of the maze.
            seed (int | None):seed for random number generation.
        """
        self._width = width
        self._height = height
        self._entry_point = entry_point
        self._exit_point = exit_point
        self._seed = seed
        self._perfect = perfect

        # 横と縦の配列の長さ
        self._w_grid = width * 2 + 1
        self._h_grid = height * 2 + 1

        self.has_ft = False
        self.ft_min_x = -1
        self.ft_max_x = -1
        self.ft_min_y = -1
        self.ft_max_y = -1

        # 横の配列を内包した縦の配列のリスト
        self._grid: list[list[int]] = [
            [Cell.ROAD.value for _ in range(self._w_grid)]
            for _ in range(self._h_grid)
        ]
        return None

    def generate(self) -> None:
        """Generate a maze."""
        # シード値(再現性の確保)
        if self._seed > 0:
            random.seed(self._seed)

        # 周りのWALL埋め込み
        self._build_outer_walls()

        # 中心に42スタンプを埋め込み
        if self._width >= 12 and self._height >= 9:
            self._build_fourty_two()

        # 柱の埋め込み→棒倒し！
        self._pillars_and_knock()

        # ex, ey: ENTRYの座標
        ex, ey = self._entry_point
        self._grid[ey * 2 + 1][ex * 2 + 1] = Cell.ENTRY.value

        # gx, gy: EXIT(ゴール)の座標
        gx, gy = self._exit_point
        self._grid[gy * 2 + 1][gx * 2 + 1] = Cell.EXIT.value
        return None


    def _build_outer_walls(self) -> None:
        """
        Build outer walls of the maze.
        """
        # y座標分ループ
        for y in range(0, self._h_grid):
            # x座標分ループ
            for x in range(0, self._w_grid):
                # 上下左右の辺にWALL埋め込み
                if y == 0 or y == self._h_grid - 1 or x == 0 or x == self._w_grid - 1:
                    self._grid[y][x] = Cell.WALL.value

    def _build_fourty_two(self) -> None:
        """
        Build the number 42 in the maze.
        """
        ft_pattern = [
            [1, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1]
        ]

        start_x = (self._width - 7) // 2
        start_y = (self._height - 5) // 2

        self.has_ft = True
        self.ft_min_x = start_x * 2
        self.ft_max_x = (start_x + 7) * 2
        self.ft_min_y = start_y * 2
        self.ft_max_y = (start_y + 5) * 2

        surrounding_offsets = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for row in range(5):
            for col in range(7):
                if ft_pattern[row][col] == 0:
                    continue
                sx = (start_x + col) * 2 + 1
                sy = (start_y + row) * 2 + 1

                self._grid[sy][sx] = Cell.FOURTY_TWO.value

                for dy, dx in surrounding_offsets:
                    self._grid[sy + dy][sx + dx] = Cell.WALL.value
        for y in range(0, self.ft_min_y):
            self._grid[y][self.ft_min_x] = Cell.WALL.value
        return None

    def _pillars_and_knock(self) -> None:
        """Place pillars and knock down walls."""
        # 追加で棒倒しをする42スタンプの左上からの相対座標
        target_pillars = [
            (4, 0), (6, 0), (4, 2), (6, 2), # 42の4の上の部分
            (0, 8), (2, 8), (0, 10), (2, 10), # 42の4の右下の部分
            (14, 10) # 42の2の右下
        ]
        for y in range(2, self._h_grid - 1, 2):
            for x in range(2, self._w_grid - 1, 2):
                if self.has_ft:
                    if x == self.ft_min_x and y < self.ft_min_y:
                        continue
                    if self.ft_min_x <= x <= self.ft_max_x and self.ft_min_y <= y <= self.ft_max_y:
                        rel_x = x - self.ft_min_x
                        rel_y = y - self.ft_min_y
                        if (rel_x, rel_y) not in target_pillars:
                            continue

                self._grid[y][x] = Cell.WALL.value

                if y == 2 and x == 2: # 一番上の一番左は左下右上(WSEN)
                    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
                elif y == 2: # 一番上のそれ以外は下右上(SEN)
                    directions = [(0, 1), (1, 0), (0, -1)]
                elif x == 2: #一番左(上記を除く)は左下右(WSE)
                    directions = [(-1, 0), (0, 1), (1, 0)]
                else: # 上から二番目、左から二番目は下右(SE)
                    directions = [(0, 1), (1, 0)]

                dx, dy = random.choice(directions)
                self._grid[y + dy][x + dx] = Cell.WALL.value


    def get_grid(self) -> list[list[int]]:
        """
        Get the grid of the maze.
        """
        return self._grid
