from dataclasses import dataclass


@dataclass
class MazeConfig:
    """
    Configuration for generating a maze.

    Attributes:
        width (int): The width of the maze.
        height (int): The height of the maze.
        entry_point (tuple[int, int]): The coordinates of the entry point.
        exit_point (tuple[int, int]): The coordinates of the exit point.
        output_file (str): The file path to save the generated maze.
        perfect (bool): Whether the maze should be perfect or not.
    """
    width: int
    height: int
    entry_point: tuple[int, int]
    exit_point: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int


def parse_config(file_path: str) -> MazeConfig:
    """
    Parses a configuration file and returns a MazeConfig object.

    Args:
        file_path (str): The path to the configuration file.

    Returns:
        MazeConfig: The parsed configuration.

    Raises:
        FileNotFoundError: If the configuration file is not found.
        ValueError: If the configuration file is invalid.
    """
    config_data = {}
    with open(file_path) as f:
        config_data= {
            key.strip().upper(): value.strip()
            for line in f
            if line.strip() and not line.strip().startswith("#") and "=" in line
            for key, value in [line.strip().split("=", 1)]
        }
    return MazeConfig(**{
        key: ope(config_data[{
            "entry_point": "entry",
            "exit_point": "exit",
        }.get(key, key).upper()])
        for key, ope in {
            "width": int,
            "height": int,
            "entry_point": lambda val: tuple(int(v) for v in val.split(',', 1)),
            "exit_point": lambda val: tuple(int(v) for v in val.split(',', 1)),
            "output_file": str,
            "perfect": lambda val: {"True": True, "False": False}.get(val),
            "seed": int
        }.items()
    })

#    try:
#    with open(file_path) as f:
#        for line in f:
#            line = line.strip()
#            if not line or line.startswith("#"):
#                continue
#            if "=" not in line:
#                raise ValueError(f"Invalid line format (missing '='): '{line}'")
#            key, value = line.split("=", 1)
#            config_data[key.strip().upper()] = value.strip()
#    except FileNotFoundError:
#        raise FileNotFoundError(f"configuration file not found: '{file_path}'")
#    except ValueError as e:
#        raise e
#     try:
#         width = int(config_data["WIDTH"]) #         height = int(config_data["HEIGHT"]) # 
#         entry_row = config_data["ENTRY"].split(",")
#         entry_point = (int(entry_row[0]), int(entry_row[1]))
#
#         exit_row = config_data["EXIT"].split(",")
#         exit_point = (int(exit_row[0]), int(exit_row[1]))
#
#         output_file = config_data["OUTPUT_FILE"]
#
#         # 小文字に変換してからチェック
#         perfect_row = config_data["PERFECT"].lower()
#         # perfectの表記ゆれ用
#         perfect = perfect_row in ("true", "1", "yes", "t")
#
#         return MazeConfig(
#             width=width,
#             height=height,
#             entry_point=entry_point,
#             exit_point=exit_point,
#             output_file=output_file,
#             perfect=perfect
#         )
#
#     except KeyError as e:
#         raise ValueError(f"Missing mandatory configration key: {e}")
#     except (ValueError, IndexError) as e:
#         raise ValueError(f"Invalid value format in configration file: {e}")
