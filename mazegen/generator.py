import random
from enum import Enum
from time import sleep
from collections import deque


# "ESC[色コードm"の順番で色付け開始、ESC[0m で色付け終了
# ESC は16進数で0x1b 8進数で033 10進数で27 の文字コード
# 1:Bold, 2:Dim, 3:Italic, 4:Underline, 5, 6: 点滅, 7:Invert
# 文字(START, GOAL)はフロント30~か90~, 空白(ROAD, WALL, FOURTY_TWO)はバック40~か100~
r_color = "\33[40m"  # 黒
w_color = "\33[107m"  # 白
s_color = "\33[1;6;91;102m"  # 赤文字、緑背景
y_color = "\33[43m"  # 黄
g_color = "\33[1;6;91;102m"  # 赤文字、緑背景
ft_color = "\33[105m"  # マゼンダ
reset = "\33[0m"


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
    ROUTE = 5


class MazeGenerator:
    """A class for generating a maze.

    Attributes:
        _width (int):width of the maze.
        _height (int):height of the maze.
        _entry_point (tuple[int, int]):entry point of the maze.
        _exit_point (tuple[int, int]):exit point of the maze.
        _seed (int | None):seed for random number generation.
        _grid (list[list[int]]):grid of the maze.
        _perfect (bool):check perfect of the maze.
    """

    def __init__(
        self,
        width: int,
        height: int,
        entry_point: tuple[int, int],
        exit_point: tuple[int, int],
        perfect: bool = False,
        seed: int | None = None,
    ) -> None:
        """Initialize the MazeGenerator.

        Args:
            width (int):Number of cells in the width of the maze.
            height (int):Number of cells in the height of the maze.
            entry_point (tuple[int, int]):entry point of the maze.
            exit_point (tuple[int, int]):exit point of the maze.
            perfect (bool):flag of the perfect maze.
            seed (int | None):seed for random number generation.
        """
        self._width = width
        self._height = height
        self._entry_point = entry_point
        self._exit_point = exit_point
        self._perfect = perfect
        self._seed = seed

        # 横と縦の配列の長さ
        self._w_grid = width * 2 + 1
        self._h_grid = height * 2 + 1

        # 42スタンプ埋め込み用
        # 横7 * 縦5 (+ 2)セル必要なのでそれ未満の時False
        self._has_ft = False
        self._ft_min_x = -1
        self._ft_max_x = -1
        self._ft_min_y = -1
        self._ft_max_y = -1

        # 横の配列 * 縦の配列のリスト(一旦ROADで埋める)
        self._grid: list[list[int]] = [
            [Cell.ROAD.value for _ in range(self._w_grid)] for _ in range(self._h_grid)
        ]

        return None

    def generate(self) -> None:
        """Generate a maze."""
        # シード値(再現性の確保)
        if self._seed > 0:
            random.seed(self._seed)

        # 全体のプリント
        self._print_maze(1)

        # 周りのWALL埋め込み、外壁のプリント
        self._build_outer_walls()
        self._print_maze(1)

        # ex, ey: ENTRYの座標
        ex, ey = self._entry_point
        self._grid[ey * 2 + 1][ex * 2 + 1] = Cell.ENTRY.value

        # gx, gy: EXIT(ゴール)の座標
        gx, gy = self._exit_point
        self._grid[gy * 2 + 1][gx * 2 + 1] = Cell.EXIT.value

        # ENTRYとEXITのプリント
        self._print_maze(1)

        # ロゴの上下左右に+ 1マス分あれば中心に42スタンプを埋め込み
        if self._width >= 9 and self._height >= 7:
            self._build_fourty_two()
            self._print_maze(1)

        # 柱の埋め込み→棒倒し！
        self._pillars_and_knock()

        return None

    print_init = False

    def _print_maze(self, sleep_time: float = 0.1) -> None:
        """
        Print the maze grid to the console.

        Args:
            maze_grid (list[list[int]]): The maze grid to print.
        """
        if not self.print_init:
            print("\x1b[2J", end="")
            print("\x1b[H", end="")
            print("\x1b[s", end="")
            self.print_init = True
        output = "\x1b[u"
        for row in self._grid:
            for cell in row:
                if cell == Cell.ROAD.value:  # 0
                    output += f"{r_color}  {reset}"
                elif cell == Cell.WALL.value:  # 1
                    output += f"{w_color}  {reset}"
                elif cell == Cell.ENTRY.value:  # 2
                    output += f"{s_color}S {reset}"
                elif cell == Cell.EXIT.value:  # 3
                    output += f"{g_color}G {reset}"
                elif cell == Cell.FOURTY_TWO.value:  # 4
                    output += f"{ft_color}  {reset}"
                elif cell == Cell.ROUTE.value:  # 5
                    output += f"{y_color}  {reset}"
            output += "\n"
        print(output)
        sleep(sleep_time)
        return None

    def solve_maze(self) -> None:
        """
        Finding the shortest path in a maze.
        """

        start = (self._entry_point[0] * 2 + 1, self._entry_point[1] * 2 + 1)
        end = (self._exit_point[0] * 2 + 1, self._exit_point[1] * 2 + 1)
        route = {}
        q = deque([start])
        while q:
            current = q.popleft()
            if current == end:
                x, y = route[end]
                while (x, y) != start:
                    self._grid[y][x] = 5
                    x, y = route[(x, y)]
                self._print_maze()
                break
            x, y = current
            for x, y in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if self._grid[y][x] in {0, 3} and (x, y) not in route:
                    q.append((x, y))
                    route[(x, y)] = current

    def _build_outer_walls(self) -> None:
        """
        Build outer walls of the maze.
        """
        # 縦配列(y) * 横配列(x) 分ループ、上下左右の辺にWALL埋め込み
        for y in range(0, self._h_grid):
            for x in range(0, self._w_grid):
                if y == 0 or y == self._h_grid - 1 or x == 0 or x == self._w_grid - 1:
                    self._grid[y][x] = Cell.WALL.value

        return None

    def _build_fourty_two(self) -> None:
        """
        Build the number 42 in the maze.
        """
        # 42スタンプパターン
        ft_pattern = [
            [1, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1],
        ]

        # 42スタンプ開始セル(切り捨て、左・上寄り)
        start_x = (self._width - 7) // 2
        start_y = (self._height - 5) // 2

        # 42スタンプ使用済みフラグ、開始座標
        self._has_ft = True
        self._ft_min_x = start_x * 2
        self._ft_max_x = (start_x + 7) * 2
        self._ft_min_y = start_y * 2
        self._ft_max_y = (start_y + 5) * 2

        # 42スタンプの周囲7マス
        surrounding_offsets = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]

        # 7 * 5 マスの内必要な場所だけスタンプ
        for row in range(5):
            for col in range(7):
                if ft_pattern[row][col] == 0:
                    continue
                sx = (start_x + col) * 2 + 1
                sy = (start_y + row) * 2 + 1

                # 42スタンプ埋め
                self._grid[sy][sx] = Cell.FOURTY_TWO.value

                # 42スタンプのセル周囲7マスを壁埋め
                for dy, dx in surrounding_offsets:
                    self._grid[sy + dy][sx + dx] = Cell.WALL.value

        return None

    def _pillars_and_knock(self) -> None:
        """Place pillars and knock down walls."""
        # 追加で棒倒しをする箇所の、42スタンプの左上からの相対座標
        target_pillars = [
            (4, 0),
            (6, 0),
            (4, 2),
            (6, 2),  # 42の4の上の部分
            (0, 8),
            (2, 8),
            (0, 10),
            (2, 10),  # 42の4の右下の部分
            (6, 10),  # 42の4の右下
            (14, 10),  # 42の2の右下
        ]
        for y in range(2, self._h_grid - 1, 2):
            for x in range(2, self._w_grid - 1, 2):
                # 42スタンプ周りの処理
                if self._has_ft:
                    # 追加で棒倒しをする箇所以外スキップ
                    if (
                        self._ft_min_x <= x <= self._ft_max_x
                        and self._ft_min_y <= y <= self._ft_max_y
                    ):
                        rel_x = x - self._ft_min_x
                        rel_y = y - self._ft_min_y
                        if (rel_x, rel_y) not in target_pillars:
                            continue

                # 柱の埋め込み
                self._grid[y][x] = Cell.WALL.value

                # perfectじゃない時は2割の確率で棒を倒さない
                if not self._perfect:
                    if random.random() > 0.8:
                        continue

                # 一番上の行の一番左は左下右上(WSEN)
                if y == 2 and x == 2:
                    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

                # 一番上の行のそれ以外は下右上(SEN)
                elif y == 2:
                    directions = [(0, 1), (1, 0), (0, -1)]

                # 一番左の列の上記以外は左下右(WSE)
                elif x == 2:
                    directions = [(-1, 0), (0, 1), (1, 0)]

                # それ以外は下右(SE)
                else:
                    directions = [(0, 1), (1, 0)]

                # 棒倒し!
                dx, dy = random.choice(directions)
                self._grid[y + dy][x + dx] = Cell.WALL.value
                self._print_maze()
        return None

    def get_grid(self) -> list[list[int]]:
        """
        Get the grid of the maze.
        """
        # 迷路の配列を返す
        return self._grid

    def get_hex_grid(self) -> list[str]:
        hex_grid = []

        for y in range(self._height):
            str_line = ""
            for x in range(self._width):
                grid_x = x * 2 + 1
                grid_y = y * 2 + 1
                cell_value = 0

                if self._grid[grid_y][grid_x - 1] in (
                    Cell.Wall.value,
                    Cell.FOURTY_TWO.value,
                ):
                    cell_value |= 8
                if self._grid[grid_y + 1][grid_x] in (
                    Cell.Wall.value,
                    Cell.FOURTY_TWO.value,
                ):
                    cell_value |= 4
                if self._grid[grid_y][grid_x + 1] in (
                    Cell.Wall.value,
                    Cell.FOURTY_TWO.value,
                ):
                    cell_value |= 2
                if self._grid[grid_y - 1][grid_x] in (
                    Cell.Wall.value,
                    Cell.FOURTY_TWO.value,
                ):
                    cell_value |= 1
                str_line += f"{cell_value:X}"

            hex_grid.append(str_line)

        return hex_grid
