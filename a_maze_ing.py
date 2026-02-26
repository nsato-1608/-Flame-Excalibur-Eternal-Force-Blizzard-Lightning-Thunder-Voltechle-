import sys
from mazegen.config import parse_config
from mazegen.generator import MazeGenerator, Cell


s_color = "\33[6;36m"
e_color = "\33[6;36m"
reset = "\33[0m"


def print_maze(maze_grid: list[list[int]]) -> None:
    for row in maze_grid:
        line = ""
        for cell in row:
            if cell == Cell.WALL.value:
                line += "💤"
            elif cell == Cell.ROAD.value:
                line += "  "
            if cell == Cell.ENTRY.value:
                line += f"{s_color}S {reset}"
            if cell == Cell.EXIT.value:
                line += f"{e_color}E {reset}"
        print(line)


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>.txt")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        """
        """
        # configにconfig.txtをパースして戻す
        config = parse_config(config_file)

        print(f"Generating a {config.width} ×{config.height} maze")
        generator = MazeGenerator(
            width=config.width,
            height=config.height,
            entry_point=config.entry_point,
            exit_point=config.exit_point,
            seed=42
        )
        generator.generate()
        print_maze(generator.get_grid())

    except (ValueError, TypeError, FileNotFoundError) as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    except KeyError as e:
        print(f"Error: missing config key: {e.args[0].upper()}")
        sys.exit(1)


if __name__ == "__main__":
    main()
