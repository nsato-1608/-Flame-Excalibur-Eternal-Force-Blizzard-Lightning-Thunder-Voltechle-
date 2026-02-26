from dataclasses import dataclass


@dataclass
class MazeConfig:
    width: int
    height: int
    entry_point: tuple[int, int]
    exit_point: tuple[int, int]
    output_file: str
    perfect: bool


def parse_config(file_path: str) -> MazeConfig:
    config_data = {}
#    try:
    with open(file_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
#            if "=" not in line:
#                raise ValueError(f"Invalid line format (missing '='): '{line}'")
            key, value = line.split("=", 1)
            config_data[key.strip().upper()] = value.strip()
#    except FileNotFoundError:
#        raise FileNotFoundError(f"configuration file not found: '{file_path}'")
#    except ValueError as e:
#        raise e
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
            "perfect": lambda val: {"True": True, "False": False}.get(val)
        }.items()
    })
# 
#     try:
# 
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
# 
