import random
from enum import Enum
from dataclasses import dataclass, field


class Cell(Enum):
    ROAD = 0
    WALL = 1
    ENTRY = 2
    EXIT = 3
    ROURTY_TWO = 4

@dataclass
class MazeData:
    width: int
    height: int
    grid: list[list[int]] = field(init=False)

    def __post_init__(self) -> None:
        if self.width % 2 == 0 or self.height % 2 == 0:
            raise ValueError("Width and height must be odd numbers for this grid responsentation.")
        self.grid = [[Cell.WALL.value for _ in range(self.width)] for _ in range(self.height)]

class MazeGenerator:
    def __init__(self, width: int, height: int, seed: int | None) -> None:
        self.maze_data = MazeData(width=width, height=height)
        self.seed = seed

    def generate(self, start_x: int = 1, start_y: int=1) -> None:
        if self.seed is not None:
            random.seed(self.seed)
        start_x = start_x if start_x % 2 != 0 else start_x +1
        start_y = start_y if start_y % 2 != 0 else start_y +1

        self._carve_passages(start_x, start_y)

        self.maze_data.grid[1][1] = Cell.ENTRY.value
        self.maze_data.grid[self.maze_data.height - 2][self.maze_data.width - 2] = Cell.EXIT.value

    def _carve_passages(self, cx: int, cy: int) -> None:
        self.maze_data.grid[cy][cx] = Cell.ROAD.value

        directions: list[tuple[int, int]] = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 1 <= nx < self.maze_data.width -1 and 1 <= ny < self.maze_data.height - 1:
                if self.maze_data.grid[ny][nx] == Cell.WALL.value:
                    self.maze_data.grid[cy + dy // 2][cx + dx // 2] = Cell.ROAD.value
                    self._carve_passages(nx, ny)

    def get_grid(self) -> list[list[int]]:
        return self.maze_data.grid

