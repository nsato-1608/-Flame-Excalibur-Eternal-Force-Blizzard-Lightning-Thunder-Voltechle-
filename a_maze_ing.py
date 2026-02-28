from sys import argv, exit
from mazegen.config import parse_config
from mazegen.generator import MazeGenerator, Cell


# ESC [ 色コード m の順番で色付け開始、ESC [ 0 m で色付け終了
# ESC は16進数で 0x1b 、8進数で 033、10進数で 27 の文字コード
# 1:Bold, 2:Dim, 3:Italic, 4:Underline, 5, 6: 点滅, 7:Invert
# 文字(START, GOAL)はフロント30~, 空白(ROAD, WALL, FOURTY_TWO)はバック40~

r_color = "\33[47m" # 白
w_color = "\33[40m" # 黒
s_color = "\33[1;6;31;42m" # 赤、緑
g_color = "\33[1;6;31;42m" # 赤、緑
ft_color = "\33[45m" # マゼンダ
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
        # configにconfig.txtをパースする。(return: MazeConfig)
        config = parse_config(config_file)

        print(f"Generating a {config.width} × {config.height} maze")
        generator = MazeGenerator(
            width=config.width,
            height=config.height,
            entry_point=config.entry_point,
            exit_point=config.exit_point,
            perfect=config.perfect,
            seed=42
        )
        generator.generate()
        print_maze(generator.get_grid())

    except (ValueError, TypeError, FileNotFoundError) as e:
        print(f"ERROR: {e}")
        exit(1)
    except KeyError as e:
        print(f"Error: missing config key: {e.args[0].upper()}")
        exit(1)


if __name__ == "__main__":
    main()
