from mazegen.generator import MazeGenerator, Cell

s_color = "\33[6;36m"
e_color = "\33[6;37m"
reset = "\33[0m"

def main():
    generator = MazeGenerator(width=21, height=21, seed=42)
    generator.generate()
    maze = generator.get_grid()

    for row in maze:
        line = ""
        for cell in row:
            if cell == Cell.WALL.value:
                line += f"💤"
            elif cell == Cell.ROAD.value:
                line += "  "
            if cell == Cell.ENTRY.value:
                line += f"{s_color}S{reset}"
            if cell == Cell.EXIT.value:
                line += f"{e_color}E{reset}"
        print(line)

if __name__ == "__main__":
    main()
