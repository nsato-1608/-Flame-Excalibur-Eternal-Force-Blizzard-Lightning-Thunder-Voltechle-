import random
from enum import Enum


class Cell(Enum):
    ROAD = 0
    WALL = 1
    ENTRY = 2
    EXIT = 3
    FOURTY_TWO = 4


class MazeGenerator:
    def __init__(self, width: int, height: int, entry_point: tuple[int, int],
            exit_point: tuple[int, int], seed: int | None = None) -> None:
        # 横のセルの個数
        self.width = width
        # 縦のセルの個数
        self.height = height

        # 2N + 1に配列を拡張
        self.w_grid = width * 2 + 1
        self.h_grid = height * 2 + 1
        self.entry_point = entry_point
        self.exit_point = exit_point

        self.seed = seed

        # リスト内のリストに1行分確保→リスト内に1列文確保
        self.grid: list[list[int]] = [
            [Cell.ROAD.value for _ in range(self.w_grid)]
            for _ in range(self.h_grid)
        ]

    def generate(self, start_x: int = 1, start_y: int=1) -> None:
        if self.seed is not None:
            random.seed(self.seed)
        self._build_outer_walls()
        self._place_pillars_and_knock_down()

        # ENTRY
        ex, ey = self.entry_point
        self.grid[ey * 2 + 1][ex * 2 + 1] = Cell.ENTRY.value

        gx, gy = self.exit_point
        self.grid[gy * 2 + 1][gx * 2 + 1] = Cell.EXIT.value

    def _build_outer_walls(self) -> None:
        for y in range(0, self.h_grid):
            for x in range(0, self.w_grid):
                if y == 0 or x == 0 or y == self.h_grid - 1 or x == self.w_grid - 1:
                    self.grid[y][x] = Cell.WALL.value

    def _place_pillars_and_knock_down(self) -> None:
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
        return self.grid

