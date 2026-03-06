"""A-Maze-ing 42.

迷路生成、出力デモ.
mazegenモジュールからMazeGeneratorをインポートし、
main()で実行する.
CLIでの操作をサポートする.

"""

from sys import argv, exit, stderr
from time import sleep
from mazegen.generator import MazeGenerator
from dataclasses import dataclass


@dataclass
class MazeConfig:
    """迷路を生成するための設定.

    Attributes:
        width (int): 迷路の幅.
        height (int): 迷路の高さ.
        entry_point (tuple[int, int]): 迷路のスタート座標.
        exit_point (tuple[int, int]): 迷路のゴール座標.
        output_file (str): 生成された迷路を保存するファイルパス.
        perfect (bool): 完全迷路にするかどうかの設定.
        seed (int): seedを元にランダムに再現性を持たせる.
        pattern (bool): 42ロゴを表示させるかの設定.
    """

    width: int
    height: int
    entry_point: tuple[int, int]
    exit_point: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int
    pattern: bool


def parse_config(file_path: str) -> MazeConfig:
    """設定ファイルを解析してMazeconfigオブジェクトを返す.

    Args:
        file_path (str): 設定ファイルへのパス.

    Returns:
        MazeConfig: 解析した設定ファイルのオブジェクト.

    Raises:
        FileNotFoundError: 設定ファイルがない場合.
        ValueError: 設定ファイルの値が無効な場合.
        KeyError: 設定ファイルのkeyが無効な場合.
        except: 上記以外のエラーが発生した場合.
    """
    config_data = {}
    with open(file_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = line.split("=", 1)
            key = key.strip().upper()
            if key in config_data:
                raise ValueError(f"Config key: '{key}' duplicated")
            config_data[key] = value.strip()

    def strtobool(val: str | None) -> bool:
        if val == "True":
            return True
        if val == "False":
            return False
        if not val:
            raise ValueError("missing config key or value")
        raise ValueError("invalid value 'True or False'")

    entry_row = config_data["ENTRY"].split(",")
    exit_row = config_data["EXIT"].split(",")

    return MazeConfig(
        width=int(config_data["WIDTH"]),
        height=int(config_data["HEIGHT"]),
        entry_point=(int(entry_row[0]), int(entry_row[1])),
        exit_point=(int(exit_row[0]), int(exit_row[1])),
        output_file=config_data["OUTPUT_FILE"],
        perfect=strtobool(config_data.get("PERFECT")),
        seed=int(config_data.get("SEED", 0)),
        pattern=strtobool(config_data.get("PATTERN", "True"))
    )


def save_to_file(
    file_path: str,
    hex_grid: list[str],
    entry_point: tuple[int, int],
    exit_point: tuple[int, int],
    path_str: str
) -> None:
    """迷路をファイルに保存する.

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
            f.write(f"{path_str}")

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

    except KeyError as e:
        print(f"Error: missing config key: {e.args[0].upper()}", file=stderr)
        exit(1)
    except FileNotFoundError:
        print("Error: No such file or dir", file=stderr)
        exit(1)
    except IsADirectoryError:
        print("Error: Is a directory", file=stderr)
        exit(1)
    except (ValueError) as e:
        print(f"Error: {e}", file=stderr)
        exit(1)
    except Exception as e:
        print(f"Error:{e}", file=stderr)
        exit(1)

    # 迷路の描画、最短経路表示、カラースキームを初期化
    needs_generation = True
    show_path = True
    color_scheme = 0
    sleep_anime = True
    print_flag = True

    while True:
        # 迷路を生成するフラグがTrueの時のみ描画処理
        if needs_generation:
            # CLIでの変更を引き継がない
            show_path = True
            color_scheme = 0
            print(f"Generating a {config.width} × {config.height} maze")
            try:
                # generatorにconfig.txtの内容送り初期化
                generator = MazeGenerator(
                    width=config.width,
                    height=config.height,
                    entry_point=config.entry_point,
                    exit_point=config.exit_point,
                    perfect=config.perfect,
                    seed=config.seed,
                    pattern=config.pattern
                )
                # 迷路生成、出力
                generator.generate(
                    sleep_anime=sleep_anime,
                    print_flag=print_flag
                )
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
                # 一度生成したらフラグを折る
                needs_generation = False
                # プリントフラグがなければここで終了
                if not print_flag:
                    return

                # 迷路描画後に最短経路表示
                sleep(1)
                generator.print_maze(show_path=show_path)

                # 42スタンプフラグがTrueかつwidthかheightが既定値以下で表示
                if config.pattern and (config.width < 9 or config.height < 7):
                    print("Pattern 42 requires a more than 8 * 6 maze size.")

            except Exception as e:
                print(f"Error: {e}", file=stderr)
                exit(1)
            except KeyboardInterrupt:
                needs_generation = False

        # ここからCLIの操作
        print("\n=== A-Maze-ing ===")

        # operations: CLIで選択できる操作一覧
        # operation: ユーザーに実際に選択された操作
        operations = {
            "1": "Re-generate",
            "2": "Show/Hide path from entry to exit "
            f"[Current: {'Show' if show_path else 'Hide'}]",
            "3": "Rotate maze colors",
            "4": "New maze size "
            f"[Current: {config.width} × {config.height}]",
            "5": f"{'un' if config.perfect else ''}perfect maze",
            "6": f"Seed value [Current: {config.seed}]",
            "7": f"42 pattern [Current: {config.pattern}]",
            "8": f"Animation [Current: {sleep_anime}]",
            "9": "Quit",
        }
        for key, value in operations.items():
            print("%s. %s" % (key, value))
        operation = ""

        # 入力を受け付ける
        # Ctrl + d か Enter の場合すぐリトライ
        try:
            choice = input("Choice? (1-9): ").strip()
        except EOFError:
            print(f"\x1b[{len(operations) + 2}A\x1b[0J", end="")
            continue
        if not choice:
            print(f"\x1b[{len(operations) + 3}A\x1b[0J", end="")
            continue

        # 指定された入力(数字)をキーとして、operationsから合う数字を取得
        # 入力がキーでない場合、値を部分一致で検索して数字を取得
        ope_list = [key for key in operations if key == choice]
        if not ope_list:
            ope_list = [
                key
                for key, command in operations.items()
                if choice.lower() in command.lower()
            ]

        # 入力と一致する選択肢が一つの時に決定
        # 入力と一致する選択肢が見つからない場合と
        # 入力が複数の選択肢と一致している場合を弾く
        if len(ope_list) == 1:
            operation = ope_list[0]
        elif len(ope_list) == 0:
            print(f"\x1b[{len(operations) + 4}A\x1b[0J", end="")
            print("Invalid choice. Please enter correct command.")
            continue
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
            # 再描画、初回はseed値0
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
            # 整数値 or Ctrl + d
            except (ValueError, EOFError):
                print(f"\x1b[{len(operations) + 4}A\x1b[0J", end="")
                print("Error: Invalid width or height value")
                continue
            if width_tmp < 2 or height_tmp < 2:
                print(f"\x1b[{len(operations) + 5}A\x1b[0J", end="")
                print("Error: Width or height value more than 2")
                continue
            if width_tmp == config.width and height_tmp == config.height:
                print(f"\x1b[{len(operations) + 5}A\x1b[0J", end="")
                print("Error: Maze size is the same as last time.")
                continue
            print(
                f"Change maze size "
                f"{config.width} × {config.height}"
                f" -> {width_tmp} × {height_tmp}"
            )
            sleep(2)
            # 再描画準備
            config.width = width_tmp
            config.height = height_tmp
            config.exit_point = (config.width - 1, config.height - 1)
            needs_generation = True
            print("\x1b[H\x1b[0J", end="")

        elif operation == "5":
            print(
                f"Change perfect "
                f"{config.perfect} -> {not config.perfect}"
            )
            sleep(2)
            # 再描画準備
            config.perfect = not config.perfect
            needs_generation = True
            print("\x1b[H\x1b[0J", end="")

        elif operation == "6":
            try:
                seed_tmp = int(input("Enter seed value: ").strip())
            # 整数値 or Ctrl + d
            except (ValueError, EOFError):
                print(f"\x1b[{len(operations) + 4}A\x1b[0J", end="")
                print("Error: Invalid seed value.")
                continue
            if seed_tmp < 0:
                print(f"\x1b[{len(operations) + 5}A\x1b[0J", end="")
                print("Error: Seed value is 0 or positive.")
                continue
            if seed_tmp == config.seed:
                print(f"\x1b[{len(operations) + 5}A\x1b[0J", end="")
                print("Error: Seed value is the same as last time.")
                continue
            print(f"Change Seed value {config.seed} -> {seed_tmp}")
            sleep(2)
            # 再描画準備
            config.seed = seed_tmp
            needs_generation = True
            print("\x1b[H\x1b[0J", end="")

        elif operation == "7":
            print(
                f"Change 42 pattern "
                f"{config.pattern} -> {not config.pattern}"
            )
            sleep(2)
            # 再描画準備
            config.pattern = not config.pattern
            needs_generation = True
            print("\x1b[H\x1b[0J", end="")

        elif operation == "8":
            print(
                f"Change animation "
                f"{sleep_anime} -> {not sleep_anime}"
            )
            sleep(2)
            # 再描画準備
            sleep_anime = not sleep_anime
            needs_generation = True
            print("\x1b[H\x1b[0J", end="")

        elif operation == "9":
            print("Exiting...")
            break

        else:
            print("\x1b[12A\x1b[0J", end="")
            print("Invalid choice. Please enter a number between 1 and 9.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
