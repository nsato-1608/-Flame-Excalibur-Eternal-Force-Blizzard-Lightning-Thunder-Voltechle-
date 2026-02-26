#!/usr/bin/env python3

import random

def mazegene():
    maze = [
        [1,1,1,1,1],
        [1,0,0,0,1],
        [1,0,1,0,1],
        [1,0,0,0,1],
        [1,0,1,0,1],
        [1,0,0,0,1],
        [1,0,1,0,1],
        [1,0,0,0,1],
        [1,1,1,1,1],
    ]

    width = 15
    height = 20


    width = width * 2 + 1
    height = height * 2 + 1
    maze = [[0] * width for _ in range(height)]

    for x in range(width):
        maze[0][x] = 1
        maze[-1][x] = 1
    for y in range(height):
        maze[y][0] = 1
        maze[y][-1] = 1

    for y in range(2, height - 1, 2):
        for x in range(2, width - 1, 2):
            if y == 2 and x == 2:
                directions = ["north", "west", "south", "east"]
            elif y == 2:
                directions = ["north", "south", "east"]
            elif x == 2:
                directions = ["west", "south", "east"]
            else:
                directions = ["south", "east"]
            while True:
                target_y, target_x = y, x
                direction = random.choice(directions)
                if direction == "north":
                    target_y -= 1
                elif direction == "south":
                    target_y += 1
                elif direction == "west":
                    target_x -= 1
                elif direction == "east":
                    target_x += 1
                if maze[target_y][target_x] == 0:
                    maze[y][x] = 1
                    maze[target_y][target_x] = 1
                    break

    return maze

def main():
    maze = mazegene()
    for line in maze:
        print(line)

main()
