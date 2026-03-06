"""迷路生成するモジュール."""
import random
from collections import deque
from enum import Enum
from time import sleep

# "ESC[色コードm"の順番で色付け開始、ESC[0m で色付け終了
# ESC は16進数で0x1b 8進数で033 10進数で27 の文字コード
# 1:Bold, 2:Dim, 3:Italic, 4:Underline, 5, 6: 点滅, 7:Invert
# 文字(START, GOAL)はフロント30~か90~, 空白(ROAD, WALL, FOURTY_TWO)はバック40~か100~
COLOR_SCHEMES = {
    0: {
        "r_color": "\33[100m",
        "w_color": "\33[107m",  # 白
        "s_color": "\33[1;6;91;102m",  # 赤文字、緑背景
        "y_color": "\33[103m",  # 黄
        "g_color": "\33[1;6;91;102m",  # 赤文字、緑背景
        "ft_color": "\33[105m",  # マゼンダ
        "reset": "\33[0m"
    },
    1: {
        "r_color": "\33[107m",  # 白
        "w_color": "\33[100m",  # 黒
        "s_color": "\33[1;6;91;102m",  # 赤文字、緑背景
        "y_color": "\33[103m",  # 黄
        "g_color": "\33[1;6;91;102m",  # 赤文字、緑背景
        "ft_color": "\33[105m",  # マゼンダ
        "reset": "\33[0m"
    },
    2: {
        "r_color": "\33[105m",
        "w_color": "\33[106m",
        "s_color": "\33[1;6;91;100m",
        "y_color": "\33[102m",
        "g_color": "\33[1;6;91;100m",
        "ft_color": "\33[103m",
        "reset": "\33[0m"
    }
}


class Cell(Enum):
    """迷路のセルの種類を設定.

    配列に格納された数値を管理するためのクラス.

    Attributes:
        ROAD (int):迷路の通路.
        WALL (int):迷路の壁.
        ENTRY (int):迷路のスタート位置.
        EXIT (int):迷路のゴール位置.
        FOURTY_TWO (int):42ロゴの位置.
    """

    ROAD = 0
    WALL = 1
    ENTRY = 2
    EXIT = 3
    FOURTY_TWO = 4
    ROUTE = 5


class MazeGenerator:
    """迷路を生成するクラス.

    Attributes:
        _width (int):迷路の幅.
        _height (int):迷路の高さ.
        _entry_point (tuple[int, int]):迷路のスタート座標.
        _exit_point (tuple[int, int]):迷路のゴール座標.
        _seed (int | None):迷路をランダムに生成するための値.
        _grid (list[list[int]]):迷路のグリッド.
        _perfect (bool):完全迷路か不完全迷路を切り替えるための値.
    """

    def __init__(
        self,
        width: int,
        height: int,
        entry_point: tuple[int, int],
        exit_point: tuple[int, int],
        perfect: bool,
        seed: int,
        pattern: bool,
    ) -> None:
        """MazeGeneratorを初期化する.

        Args:
            width (int):迷路の幅.
            height (int):迷路の高さ.
            entry_point (tuple[int, int]):迷路のスタート座標.
            exit_point (tuple[int, int]):迷路のゴール座標.
            perfect (bool):完全迷路か不完全迷路を切り替えるための値.
            seed (int):迷路をランダムに生成するための値.
            pattern (bool): 42ロゴの生成を切り替えるための値.
        """
        self._width = width
        self._height = height
        self._entry_point = entry_point
        self._exit_point = exit_point
        self._perfect = perfect
        self._seed = seed
        self._pattern = pattern

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
            [Cell.ROAD.value] * self._w_grid
            for _ in range(self._h_grid)
        ]

    def generate(
        self,
        sleep_anime: bool = False,
        print_flag: bool = False
    ) -> None:
        """迷路を生成する.

        Args:
            sleep_anime (bool):アニメーション実行フラグ.
            print_flag (bool):ターミナル描画フラグ.
        """
        # 横の配列 * 縦の配列のリスト(一旦ROADで埋める)
        self._grid: list[list[int]] = [
            [Cell.ROAD.value] * self._w_grid
            for _ in range(self._h_grid)
        ]
        # シード値(再現性の確保)
        if self._seed > 0:
            random.seed(self._seed)
        # ターミナル描画モード時、50×50以上はエラーにする
        if print_flag and (self._width > 49 or self._height > 49):
            raise ValueError("The maze is too large. It cannnot be drawn.")
        # ex, ey: ENTRYの座標
        ex, ey = self._entry_point
        # gx, gy: EXIT(ゴール)の座標(範囲外アクセスの可能性)
        gx, gy = self._exit_point
        # ENTRY_POINT, EXIT_POINTの有効値チェック
        if ex == gx and ey == gy:
            raise ValueError(
                "ENTRY_POINT and EXIT_POINT are at the same coordinates"
            )
        if ex < 0 or ey < 0:
            raise ValueError("ENTRY_POINT is not minus value")
        if gx < 0 or gy < 0:
            raise ValueError("EXIT_POINT is not minus value")

        # ENTRY, EXIT埋め込み
        self._grid[ey * 2 + 1][ex * 2 + 1] = Cell.ENTRY.value
        self._grid[gy * 2 + 1][gx * 2 + 1] = Cell.EXIT.value

        # 周りのWALL埋め込み
        self._build_outer_walls(
            sleep_anime=sleep_anime,
            print_flag=print_flag
        )
        # ロゴの上下左右に+ 1マス分あれば中心に42スタンプを埋め込み
        if self._width >= 9 and self._height >= 7 and self._pattern:
            self._build_fourty_two(
                sleep_anime=sleep_anime,
                print_flag=print_flag
            )
        # 柱の埋め込み→棒倒し！
        self._pillars_and_knock(
            sleep_anime=sleep_anime,
            print_flag=print_flag
        )
        if print_flag:
            self.print_maze()
        return None

    def _build_outer_walls(
        self,
        sleep_anime: bool = False,
        print_flag: bool = False
    ) -> None:
        """迷路の外壁を生成する.

        Args:
            sleep_anime (bool):アニメーション実行フラグ.
            print_flag (bool):ターミナル描画フラグ.
        """
        # 縦配列(y) * 横配列(x) 分ループ、上下左右の辺にWALL埋め込み
        for y in range(0, self._h_grid):
            for x in range(0, self._w_grid):
                if (
                    y == 0 or y == self._h_grid - 1
                    or x == 0 or x == self._w_grid - 1
                ):
                    self._grid[y][x] = Cell.WALL.value

        if print_flag and sleep_anime:
            self.print_maze(1.0)
        return None

    def _build_fourty_two(
        self,
        sleep_anime: bool = False,
        print_flag: bool = False
    ) -> None:
        """迷路の中に42ロゴを生成する.

        Args:
            sleep_anime (bool):アニメーション実行フラグ.
            print_flag (bool):ターミナル描画フラグ.
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

        # 42スタンプ使用済みフラグ、開始座標、終了座標
        self._has_ft = True
        self._ft_min_x = start_x * 2
        self._ft_max_x = (start_x + 7) * 2
        self._ft_min_y = start_y * 2
        self._ft_max_y = (start_y + 5) * 2

        # 42スタンプの周囲7マス
        surrounding_offsets = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1),
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

        # アニメーション処理
        if print_flag and sleep_anime:
            self.print_maze(1.0)
        return None

    def _pillars_and_knock(
        self,
        sleep_anime: bool = False,
        print_flag: bool = False
    ) -> None:
        """棒倒し方のアルゴリズム.

        Args:
            sleep_anime (bool):アニメーション実行フラグ.
            print_flag (bool):ターミナル描画フラグ.
        """
        # 追加で棒倒しをする箇所の、42スタンプの左上からの相対座標
        target_pillars = [
            (4, 0), (6, 0), (4, 2), (6, 2),  # 42の4の上の部分
            (0, 8), (2, 8), (0, 10), (2, 10),  # 42の4の右下の部分
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

                # 基本処理
                # 柱の埋め込み
                self._grid[y][x] = Cell.WALL.value

                # perfectじゃないかつ柱の左と上に棒が倒れている時
                # 4割の確率で棒を倒さない
                if (not self._perfect and random.random() > 0.6
                   and (self._grid[y - 1][x] is Cell.WALL.value
                   or self._grid[y][x - 1] is Cell.WALL.value)):
                    continue

                # 基本は右と下に倒す(SとE)
                directions = [(0, 1), (1, 0)]
                # 一番左なら左にも倒す(W)
                if x == 2:
                    directions.append((-1, 0))
                # 一番上なら上にも倒す(N)
                if y == 2:
                    directions.append((0, -1))

                # 棒倒し!
                dx, dy = random.choice(directions)
                self._grid[y + dy][x + dx] = Cell.WALL.value
                if print_flag and sleep_anime:
                    self.print_maze(0.05)
        return None

    print_init = False

    def print_maze(
        self, sleep_time: float = 0.0,
        show_path: bool = False,
        color_id: int = 0
    ) -> None:
        """コンソールに迷路を出力する.

        Args:
            sleep_time (flat): プロセスの実行を遅らせるための値.
            show_path (bool): ゴールまでの経路表示の切り替えをする値.
            color_id (int): 迷路のカラープリセットを選ぶ値.
            maze_grid (list[list[int]]): 出力するための迷路.
        """
        colors = COLOR_SCHEMES.get(color_id, COLOR_SCHEMES[0])
        r_color = colors["r_color"]
        w_color = colors["w_color"]
        s_color = colors["s_color"]
        y_color = colors["y_color"]
        g_color = colors["g_color"]
        ft_color = colors["ft_color"]
        reset = colors["reset"]

        if not self.print_init:
            print("\x1b[2J\x1b[H\x1b[s", end="")
            self.print_init = True
        output = "\x1b[H\x1b[0J"
        for row in self._grid:
            for cell in row:
                if (
                    cell is Cell.ROAD.value or
                    (cell is Cell.ROUTE.value and not show_path)
                ):
                    output += f"{r_color}  {reset}"
                elif cell is Cell.WALL.value:
                    output += f"{w_color}  {reset}"
                elif cell is Cell.ENTRY.value:
                    output += f"{s_color}S {reset}"
                elif cell is Cell.EXIT.value:
                    output += f"{g_color}G {reset}"
                elif cell is Cell.FOURTY_TWO.value:
                    output += f"{ft_color}  {reset}"
                elif cell is Cell.ROUTE.value:
                    output += f"{y_color}  {reset}"
            output += "\n"

        print(output)
        sleep(sleep_time)

        return None

    def solve_maze(self) -> str:
        """幅優先探索でゴールまでの最短経路を求める.

        Returns:
            str: ゴールまでの道筋を'N', 'E', 'S', 'W'で表す.
        """
        start = (self._entry_point[0] * 2 + 1, self._entry_point[1] * 2 + 1)
        end = (self._exit_point[0] * 2 + 1, self._exit_point[1] * 2 + 1)
#        route = {start: None}
        route: dict[tuple[int, int], tuple[int, int]] = {}
        q = deque([start])
        while q:
            current = q.popleft()

            if current == end:
                path_coords = [end]
                curr = end
                while curr != start:
                    curr = route[curr]
                    path_coords.append(curr)

                path_coords.reverse()

                path_str = ""

                for i in range(0, len(path_coords) - 1, 2):
                    cx, cy = path_coords[i]
                    nx, ny = path_coords[i + 2]

                    if nx > cx:
                        path_str += "E"
                    elif nx < cx:
                        path_str += "W"
                    elif ny > cy:
                        path_str += "S"
                    elif ny < cy:
                        path_str += "N"

                x, y = route[end]
                while (x, y) != start:
                    self._grid[y][x] = Cell.ROUTE.value
                    x, y = route[(x, y)]
                return path_str

            cx, cy = current
            for nx, ny in (
                (cx - 1, cy),
                (cx + 1, cy),
                (cx, cy - 1),
                (cx, cy + 1)
            ):
                if (self._grid[ny][nx] in {Cell.ROAD.value, Cell.EXIT.value}
                   and (nx, ny) not in route):
                    q.append((nx, ny))
                    route[(nx, ny)] = current
        return ""

    def get_grid(self) -> list[list[int]]:
        """迷路の配列を返す."""
        # 迷路の配列を返す
        return self._grid

    def get_hex_grid(self) -> list[str]:
        """迷路を16進数に変換する."""
        hex_grid = []

        for y in range(self._height):
            str_line = ""
            for x in range(self._width):
                grid_x = x * 2 + 1
                grid_y = y * 2 + 1
                cell_value = 0
                for val, cell in (
                    (0b0001, self._grid[grid_y - 1][grid_x]),
                    (0b0010, self._grid[grid_y][grid_x + 1]),
                    (0b0100, self._grid[grid_y + 1][grid_x]),
                    (0b1000, self._grid[grid_y][grid_x - 1])
                ):
                    if cell in {Cell.WALL.value, Cell.FOURTY_TWO.value}:
                        cell_value |= val

                str_line += f"{cell_value:X}"
            hex_grid.append(str_line)
        return hex_grid
