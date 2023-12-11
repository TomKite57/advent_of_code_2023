
def load_file(filename):
    with open(filename, 'r') as file:
        data = [[c for c in line.strip()] for line in file]
    return data

def get_start(maze):
    for y, row in enumerate(maze):
        for x, elem in enumerate(row):
            if elem == "S":
                return (x, y)
    return (None, None)

def walk_maze(maze):
    start = get_start(maze)
    history = dict()
    paths = [(start, 0), ]

    while len(paths):
        pos, length = paths.pop()
        x, y = pos
        if pos in history and history[pos] <= length:
            continue
        pipe = maze[y][x]

        history[pos] = length
        north = ((pos[0], pos[1]-1), length+1) if pos[1]-1 >= 0 else None
        south = ((pos[0], pos[1]+1), length+1) if pos[1]+1 < len(maze) else None
        west = ((pos[0]-1, pos[1]), length+1) if pos[0]-1 >= 0 else None
        east = ((pos[0]+1, pos[1]), length+1) if pos[0]+1 < len(maze[0]) else None

        if pipe == "|":
            paths.extend([north, south])
        elif pipe == "-":
            paths.extend([west, east])
        elif pipe == "J":
            paths.extend([north, west])
        elif pipe == "F":
            paths.extend([south, east])
        elif pipe == "L":
            paths.extend([north, east])
        elif pipe == "7":
            paths.extend([west, south])
        elif pipe == "S":
            if maze[y][x+1] in ["J", "-", "7"]:
                paths.append(east)
            if maze[y][x-1] in ["F", "L", "-"]:
                paths.append(west)
            if maze[y-1][x] in ["F", "7", "|"]:
                paths.append(north)
            if maze[y+1][x] in ["J", "L", "|"]:
                paths.append(south)

    return history

def get_clean_maze(maze, history):
    new_maze = [[x for x in row] for row in maze]
    for y, row in enumerate(new_maze):
        for x, elem in enumerate(row):
            if (x, y) not in history:
                new_maze[y][x] = '.'
    return new_maze

def expand_maze(maze):
    new_maze = [['.' for _ in row*3] for row in maze*3]

    def fill_with(xx, yy, elems):
        for i, row in enumerate(elems):
            for j, elem in enumerate(row):
                new_maze[yy-1+i][xx-1+j] = elem

    for y, row in enumerate(maze):
        yy = 3*y + 1
        for x, elem in enumerate(row):
            xx = 3*x + 1

            if elem == ".":
                fill_with(xx, yy, ['...', '...', '...'])
            elif elem == "-":
                fill_with(xx, yy, ['...', '---', '...'])
            elif elem == "|":
                fill_with(xx, yy, ['.|.', '.|.', '.|.'])
            elif elem == "F":
                fill_with(xx, yy, ['...', '.F-', '.|.'])
            elif elem == "L":
                fill_with(xx, yy, ['.|.', '.L-', '...'])
            elif elem == "J":
                fill_with(xx, yy, ['.|.', '-J.', '...'])
            elif elem == "7":
                fill_with(xx, yy, ['...', '-7.', '.|.'])

    return new_maze

def replace_start(maze):
    x, y = get_start(maze)

    if maze[y-1][x] in "|7F" and maze[y][x-1] in "-LF":
        maze[y][x] = 'J'
    elif maze[y-1][x] in "|7F" and maze[y][x+1] in "-J7":
        maze[y][x] = 'L'
    elif maze[y+1][x] in "|LJ" and maze[y][x-1] in "-LF":
        maze[y][x] = '7'
    elif maze[y+1][x] in "|LJ" and maze[y][x+1] in "-J7":
        maze[y][x] = 'F'
    else:
        raise Exception("What the ****")

    return maze

def build_3x_out_tiles(maze, history):
    seen = set()
    paths = [(0,0), ]

    while len(paths):
        x, y = paths.pop()
        if (x, y) in seen:
            continue
        seen.add((x, y))

        north = (x,   y-1) if y-1 >= 0 else None
        south = (x,   y+1) if y+1 < len(maze) else None
        west  = (x-1, y  ) if x-1 >= 0 else None
        east  = (x+1, y  ) if x+1 < len(maze[0]) else None

        for new_pos in [north, south, east, west]:
            if new_pos is None:
                continue
            xx, yy = new_pos
            if maze[yy][xx] == ".":
                paths.append(new_pos)

    return seen

def count_in(maze, history, out_3x):
    count = 0
    for y, row in enumerate(maze):
        for x, elem in enumerate(row):
            if (x, y) in history:
                continue
            if (3*x+1, 3*y+1) in out_3x:
                continue
            count += 1
    return count

def main():
    maze = load_file("data/day_10.txt")
    maze_walk = walk_maze(maze)

    checksum_1 = max(maze_walk.values())
    print(f"Part 1\n{checksum_1}")

    new_maze = replace_start(maze)
    new_maze = get_clean_maze(new_maze, maze_walk)
    new_maze = expand_maze(new_maze)
    out_tiles_3x = build_3x_out_tiles(new_maze, maze_walk)
    checksum_2 = count_in(maze, maze_walk, out_tiles_3x)
    print(f"Part 2\n{checksum_2}")


    #for y, row in enumerate(new_maze):
    #    for x, elem in enumerate(row):
    #        if (x, y) in out_tiles_3x:
    #            print("O", end="")
    #        else:
    #            print(elem, end="")
    #    print()

if __name__ == "__main__":
    main()