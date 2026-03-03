from imaplib import Commands
from sys import argv, exit, stderr
from time import sleep
from tkinter import TclError

from mazegen.config import parse_config
from mazegen.generator import MazeGenerator


def save_to_file(
        file_path: str,
        hex_grid: list[str],
        entry_point: tuple[int, int],
        exit_point: tuple[int, int],
        path_str: str
        ) -> None:
    """
    Saves the maze to a file.

    Args:
        file_path (str): Path to the file to save.
        hex_grid (list[str]): Hex grid representation of the maze.
        entry_point (tuple[int, int]): Entry point coordinates.
        exit_point (tuple[int, int]): Exit point coordinates.
        path_str (str, optional): Path string.
    """

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            for row in hex_grid:
                f.write(f"{row}\n")
            f.write("\n")

            f.write(f"{entry_point[0]},{entry_point[1]}\n")
            f.write(f"{exit_point[0]}, {exit_point[1]}\n")
            f.write(f"{path_str}\n")

    except OSError as e:
        print(f"Error: Failed to save the maze to '{file_path}'."
              f"Details: {e}", file=stderr)


def main() -> None:
    """
    Main function for testing maze generation
    """
    # 引数が2個でない時にエラー
    if len(argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>.txt", file=stderr)
        exit(1)

    config_file = argv[1]
    try:
        # configにconfig.txtをパースする(MazeConfigクラスが返ってくる)
        config = parse_config(config_file)

    except KeyError as e:
        print(f"Error: missing config key: {e.args[0].upper()}", file=stderr)
        exit(1)
    except (ValueError, TypeError, FileNotFoundError) as e:
        print(f"ERROR: {e}", file=stderr)
        exit(1)

    needs_generation = True
    show_path = False
    color_scheme = 0
    width_value = config.width
    height_value = config.height
    exit_value = config.exit_point
    perfect_value = config.perfect
    seed_value = config.seed
    pattern_value = config.pattern

    while True:
        if needs_generation:
            show_path = False
            color_scheme = 0
            print(f"Generating a {config.width} × {config.height} maze")
            try:
                # generatorにconfig.txtの内容送り初期化
                generator = MazeGenerator(
                    width=width_value,
                    height=height_value,
                    entry_point=config.entry_point,
                    exit_point=exit_value,
                    perfect=perfect_value,
                    seed=seed_value,
                    pattern=pattern_value
                )
                # 迷路生成、出力
                generator.generate()
                # 最短経路受け取り
                path_str = generator.solve_maze()
                # 16進数の文字列リスト受け取り
                hex_grid = generator.get_hex_grid()
                # output_file(maze.txt)に情報書き込み
                save_to_file(
                    file_path=config.output_file,
                    hex_grid=hex_grid,
                    entry_point=config.entry_point,
                    exit_point=config.exit_point,
                    path_str=path_str
                        )
                needs_generation = False
                generator.print_maze(show_path)

            except Exception as e:
                print(f"ERROR: {e}", file=stderr)
                exit(1)
        operations = {
            "1": "Re-generate a new maze",
            "2": "Show/Hide path from entry to exit",
            "3": "Rotate maze colors",
            "4": "Set new maze size",
            "5": f"Set {'un' if perfect_value else ''}perfect maze",
            "6": "Set seed value",
            "7": "Set 42 pattern",
            "8": "Quit",
        }
        print("\n=== A-Maze-ing ===")
        for key, value in operations.items():
            print("%s. %s" % (key, value))
#        print("1. Re-generate a new maze")
#        print("2. Show/Hide path from entry to exit")
#        print("3. Rotate maze colors")
#        print("4. Set new maze size")
#        print(f"5. Set {'un' if perfect_value else ''}perfect maze")
#        print("6. Set seed value")
#        print("7. Set 42 pattern")
#        print("8. Quit")

        operation = 0
        try:
            choice = input("Choice? (1-8): ").strip()
        except EOFError:
            print(f"\x1b[{len(operations) + 2}A\x1b[0J", end="")
            continue

        if not choice:
            print(f"\x1b[{len(operations) + 3}A\x1b[0J", end="")
            continue
        ope_list = [key for key in operations if key == choice]
        if not ope_list:
            ope_list = [key for key, command in operations.items() if choice.lower() in command.lower()]
        if len(ope_list) == 1:
           operation = ope_list[0]
        elif len(ope_list) == 0:
            print(f"\x1b[{len(operations) + 4}A\x1b[0J", end="")
            print("Invalid choice. Please enter correct command.")
            continue
        elif len(ope_list) > 1:
            print(f"\x1b[{len(operations) + 4}A\x1b[0J", end="")
            print(f"command conflict with multiple operations: {', '.join('%s: %s' % (key, operations[key]) for key in ope_list)}. Please enter correct command.")
            continue

        if operation == "1":
            needs_generation = True
            continue
        elif operation == "2":
            show_path = not show_path
            print("\x1b[H\x1b[0J", end="")
            generator.print_maze(0, show_path, color_scheme)
        elif operation == "3":
            color_scheme = (color_scheme + 1) % 3
            print("\x1b[H\x1b[0J", end="")
            generator.print_maze(0, show_path, color_scheme)
        elif operation == "4":
            width_value = int(input("Enter width value: ").strip())
            height_value = int(input("Enter height value: ").strip())
            exit_value = (width_value - 1, height_value - 1)
            needs_generation = True
            print("\x1b[H\x1b[0J", end="")
            generator.print_maze(0, show_path, color_scheme)
        elif operation == "5":
            perfect_value = not perfect_value
            print(f"Change perfect {not perfect_value} -> {perfect_value}")
            sleep(2)
            needs_generation = True
            print("\x1b[H\x1b[0J", end="")
            generator.print_maze(0, show_path, color_scheme)
        elif operation == "6":
            try:
                seed_value = int(input("Enter seed value: ").strip())
            except (ValueError, EOFError):
                print(f"\x1b[{len(operations) + 4}A\x1b[0J", end="")
                print("Error: invalid seed value")
                continue
            needs_generation = True
            print("\x1b[H\x1b[0J", end="")
            generator.print_maze(0, show_path, color_scheme)
        elif operation == "7":
            pattern_value = not pattern_value
            print(f"Change 42 pattern {not pattern_value} -> {pattern_value}")
            sleep(2)
            needs_generation = True
            print("\x1b[H\x1b[0J", end="")
            generator.print_maze(0, show_path, color_scheme)
        elif operation == "8":
            print("Exiting...")
            break
        else:
            print("\x1b[12A\x1b[0J", end="")
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
