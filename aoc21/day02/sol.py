# -*- coding: utf-8 -*-
pos = dict()
vert = 0
hor = 0

with open("input.txt") as f:
    for line in f:
        commands = line.split()
        if commands[0] == "forward":
            hor += int(commands[1])
        elif commands[0] == "down":
            vert += int(commands[1])
        elif commands[0] == "up":
            vert -= int(commands[1])
        else:
            raise ValueError("ARGH!")

print(vert * hor)

aim = 0
vert = 0
hor = 0

with open("input.txt") as f:
    for line in f:
        commands = line.split()
        if commands[0] == "forward":
            hor += int(commands[1])
            vert += aim * int(commands[1])
        elif commands[0] == "down":
            aim += int(commands[1])
        elif commands[0] == "up":
            aim -= int(commands[1])
        else:
            raise ValueError("ARGH!")


print(vert * hor)
