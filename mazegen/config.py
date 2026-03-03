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
    pattern: bool


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
        config_data = {
            key.strip().upper(): value.strip()
            for line in f
            if (line.strip()
                and not line.strip().startswith("#")
                and "=" in line)
            for key, value in [line.strip().split("=", 1)]
        }
    from typing import Callable
    def strtobool() -> Callable[[str], bool | None]:
        return lambda val: {"True": True, "False": False}.get(val)
    return MazeConfig(**{
        key: ope(config_data[{
                "entry_point": "entry",
                "exit_point": "exit",
            }.get(key, key).upper()])
            for key, ope in {
                "width": int,
                "height": int,
                "entry_point": lambda val:
                    tuple(int(v) for v in val.split(',', 1)),
                "exit_point": lambda val:
                    tuple(int(v) for v in val.split(',', 1)),
                "output_file": str,
                "perfect": strtobool()
            }.items()
        }, **{
            key: ope(config_data.get(key.upper(), default))
            for key, (ope, default) in {
                "seed": (int, 0),
                "pattern": (strtobool(), "True")
            }.items()
        }
    )
