from sys import argv, exit
from mazegen.config import parse_config
from mazegen.generator import MazeGenerator, Cell


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

    except (ValueError, TypeError, FileNotFoundError) as e:
        print(f"ERROR: {e}")
        exit(1)
    except KeyError as e:
        print(f"Error: missing config key: {e.args[0].upper()}")
        exit(1)


if __name__ == "__main__":
    main()
