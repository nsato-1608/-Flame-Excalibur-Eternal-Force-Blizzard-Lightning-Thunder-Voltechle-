from sys import argv, exit
from mazegen.config import parse_config
from mazegen.generator import MazeGenerator, Cell
from time import sleep


# "ESC[色コードm"の順番で色付け開始、ESC[0m で色付け終了
# ESC は16進数で0x1b 8進数で033 10進数で27 の文字コード
# 1:Bold, 2:Dim, 3:Italic, 4:Underline, 5, 6: 点滅, 7:Invert
# 文字(START, GOAL)はフロント30~か90~, 空白(ROAD, WALL, FOURTY_TWO)はバック40~か100~
r_color = "\33[40m" # 黒
w_color = "\33[107m" # 白
s_color = "\33[1;6;91;102m" # 赤文字、緑背景
g_color = "\33[1;6;91;102m" # 赤文字、緑背景
ft_color = "\33[105m" # マゼンダ
reset = "\33[0m"


def print_maze(maze_grid: list[list[int]]) -> None:
    """
    Print the maze grid to the console.

    Args:
        maze_grid (list[list[int]]): The maze grid to print.
    """
    for row in maze_grid:
        line = ""
        for cell in row:
            if cell == Cell.ROAD.value: # 0
                line += f"{r_color}  {reset}"
            elif cell == Cell.WALL.value: # 1
                line += f"{w_color}  {reset}"
            elif cell == Cell.ENTRY.value: # 2
                line += f"{s_color}S {reset}"
            elif cell == Cell.EXIT.value: # 3
                line += f"{g_color}G {reset}"
            elif cell == Cell.FOURTY_TWO.value: # 4
                line += f"{ft_color}  {reset}"
        print(line)


def main() -> None:
    """
    Main function for testing maze generation
    """
    if len(argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>.txt")
        sys.exit(1)

    config_file = argv[1]
    try:
        # configにconfig.txtをパースする(MazeConfigクラスが返ってくる)
        config = parse_config(config_file)

        print(f"Generating a {config.width} × {config.height} maze")

        # generatorにconfig.txtの内容送り初期化
        generator = MazeGenerator(
            width=config.width,
            height=config.height,
            entry_point=config.entry_point,
            exit_point=config.exit_point,
            perfect=config.perfect,
            seed=42
        )
        # 迷路生成
        generator.generate()
        # 迷路出力
        print_maze(generator.get_grid())

    except (ValueError, TypeError, FileNotFoundError) as e:
        print(f"ERROR: {e}")
        exit(1)
    except KeyError as e:
        print(f"Error: missing config key: {e.args[0].upper()}")
        exit(1)


if __name__ == "__main__":
    main()
