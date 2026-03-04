"""A-Maze-ing 42.

迷路生成、出力デモ.
mazegenモジュールからMazeGeneratorをインポートし、
main()で実行する.
CLIでの操作をサポートする.

"""

from sys import argv, exit, stderr
from time import sleep

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
    迷路をファイルに保存する.

    Args:
        file_path (str): 保存するファイルパス
        hex_grid (list[str]): 迷路のHexGrid
        entry_point (tuple[int, int]): 入口の座標
        exit_point (tuple[int, int]): 出口の座標
        path_str (str): 迷路のパス
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            for row in hex_grid:
                f.write(f"{row}\n")
            f.write("\n")

            f.write(f"{entry_point[0]},{entry_point[1]}\n")
            f.write(f"{exit_point[0]},{exit_point[1]}\n")
            f.write(f"{path_str}\n")

    except OSError as e:
        print(f"Error: Failed to save the maze to '{file_path}'."
              f"Details: {e}", file=stderr)


def main() -> None:
    """迷路生成デモメイン関数."""
    # 引数が2個でない時にエラー
    if len(argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>.txt", file=stderr)
        exit(1)

    config_file = argv[1]
    try:
        # configにconfig.txtをパースする(MazeConfigクラスが返ってくる)
        config = parse_config(config_file)
        # フラグと値の初期化
        needs_generation = True
        show_path = False
        color_scheme = 0
        config.validate()
        configs = config.copy()
#        configs.width = config.width
#        configs.height = config.height
#        configs.entry = config.entry_point
#        configs.exit = config.exit_point
#        configs.perfect = config.perfect
#        configs.seed = config.seed
#        configs.pattern = config.pattern

    except KeyError as e:
        print(f"Error: missing config key: {e.args[0].upper()}", file=stderr)
        exit(1)
    except (ValueError, TypeError, FileNotFoundError) as e:
        print(f"ERROR: {e}", file=stderr)
        exit(1)


    while True:
        if needs_generation:
            show_path = False
            color_scheme = 0
            print(f"Generating a {config.width} × {config.height} maze")
            try:
                # generatorにconfig.txtの内容送り初期化
                generator = MazeGenerator(
                    width=configs.width,
                    height=configs.height,
                    entry_point=configs.entry_point,
                    exit_point=configs.exit_point,
                    perfect=configs.perfect,
                    seed=configs.seed,
                    pattern=configs.pattern
#                    **vars(configs)
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
                    entry_point=configs.entry_point,
                    exit_point=configs.exit_point,
                    path_str=path_str
                        )
                # 一度生成したらフラグをおる
                needs_generation = False
                generator.print_maze(show_path)
                if (configs.width < 9 or configs.height < 7) and configs.pattern:
                    print("Pattern 42 requires a more than 8 * 6 maze size.")

            except Exception as e:
                print(f"ERROR: {e}", file=stderr)
                exit(1)

        # CLIでの操作選択
        operations = {
            "1": "Re-generate a new maze",
            "2": "Show/Hide path from entry to exit",
            "3": "Rotate maze colors",
            "4": "Set new maze size",
            "5": f"Set {'un' if configs.perfect else ''}perfect maze",
            "6": "Set seed value",
            "7": "Set 42 pattern",
            "8": "Quit",
        }

        print("\n=== A-Maze-ing ===")
        for key, value in operations.items():
            print("%s. %s" % (key, value))

        operation = 0
        try:
            # 入力を受け付ける
            choice = input("Choice? (1-8): ").strip()
        except EOFError:
            print(f"\x1b[{len(operations) + 2}A\x1b[0J", end="")
            continue

        # 何も選択されなかった場合すぐリトライ
        if not choice:
            print(f"\x1b[{len(operations) + 3}A\x1b[0J", end="")
            continue

        # 指定された入力(数字)をキーとして、operationsから合う数字を取得
        ope_list = [key for key in operations if key == choice]
        if not ope_list:
            # 入力がキーでない場合、値を部分一致で検索して数字を取得
            ope_list = [
                key
                for key, command in operations.items()
                if choice.lower() in command.lower()
            ]

        if len(ope_list) == 1:
            operation = ope_list[0]

        # 入力が一致する数字が見つからない場合の処理
        elif len(ope_list) == 0:
            print(f"\x1b[{len(operations) + 4}A\x1b[0J", end="")
            print("Invalid choice. Please enter correct command.")
            continue

        # 入力が複数の数字と一致する場合の処理
        elif len(ope_list) > 1:
            print(f"\x1b[{len(operations) + 4}A\x1b[0J", end="")
            print(
                "command conflict with multiple operations: "
                f"""{', '.join(
                    '%s: %s' % (key, operations[key]) for key in ope_list
                )}."""
                "Please enter correct command."
            )
            continue

        if operation == "1":
            needs_generation = True
            continue

        elif operation == "2":
            show_path = not show_path
            print("\x1b[H\x1b[0J", end="")
            # その場ですぐ表示
            generator.print_maze(0, show_path, color_scheme)

        elif operation == "3":
            color_scheme = (color_scheme + 1) % 3
            print("\x1b[H\x1b[0J", end="")
            # その場ですぐ表示
            generator.print_maze(0, show_path, color_scheme)

        elif operation == "4":
            try:
                width_tmp = int(input("Enter width value: ").strip())
                height_tmp = int(input("Enter height value: ").strip())
            except (ValueError, EOFError):
                print(f"\x1b[{len(operations) + 4}A\x1b[0J", end="")
                print("Error: invalid width or height value")
                continue
            if width_tmp < 2 or height_tmp < 2:
                print(f"\x1b[{len(operations) + 5}A\x1b[0J", end="")
                print("Error: width or height value more than 2")
                continue
            configs.width = width_tmp
            configs.height = height_tmp
            configs.exit = (configs.width - 1, configs.height - 1)
            needs_generation = True
            print("\x1b[H\x1b[0J", end="")
            generator.print_maze(0, show_path, color_scheme)

        elif operation == "5":
            configs.perfect = not configs.perfect
            print(f"Change perfect {not configs.perfect} -> {configs.perfect}")
            sleep(2)
            needs_generation = True
            print("\x1b[H\x1b[0J", end="")
            generator.print_maze(0, show_path, color_scheme)

        elif operation == "6":
            try:
                configs.seed = int(input("Enter seed value: ").strip())
            except (ValueError, EOFError):
                print(f"\x1b[{len(operations) + 4}A\x1b[0J", end="")
                print("Error: invalid seed value")
                continue
            needs_generation = True
            print("\x1b[H\x1b[0J", end="")
            generator.print_maze(0, show_path, color_scheme)

        elif operation == "7":
            configs.pattern = not configs.pattern
            print(f"Change 42 pattern {not configs.pattern} -> {configs.pattern}")
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
