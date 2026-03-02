from sys import argv, stderr, exit
from mazegen.config import parse_config
from mazegen.generator import MazeGenerator, Cell

def save_to_file(
        file_path: str,
        hex_grid: list[str],
        entry_point: tuple[int, int],
        exit_point: tuple[int, int],
        path_str: str = "WIP"
    ) -> None:

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            for row in hex_grid:
                f.write(f"{row}\n")
            f.write("\n")
            f.write("")

            f.write(f"{entry_point[0]},{entry_point[1]}\n")
            f.write(f"{exit_point[0]}, {exit_point[1]}\n")
            f.write(f"{path_str}\n")

    except OSError as e:
        print(f"Error: Failed to save the maze to '{file_path}'. Details: {e}", file=stderr)

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
            seed=config.seed
        )
        # 迷路生成、出力
        generator.generate()
        # 16進数の文字列リスト受け取り
        hex_grid = generator.get_hex_grid()

        # output_file(maze.txt)に情報書き込み
        save_to_file(
            file_path=config.output_file,
            hex_grid=hex_grid,
            entry_point=config.entry_point,
            exit_point=config.exit_point
                )

    except (ValueError, TypeError, FileNotFoundError) as e:
        print(f"ERROR: {e}", file=stderr)
        exit(1)
    except KeyError as e:
        print(f"Error: missing config key: {e.args[0].upper()}", file=stderr)
        exit(1)


if __name__ == "__main__":
    main()
