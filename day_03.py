
import itertools


def load_file(fname):
    with open(fname, 'r') as file:
        data = [[c for c in line.strip()] for line in file]
    return data


def is_digit(x):
    try:
        int(x)
        return True
    except ValueError:
        return False


def get_sort_key(schematic):
    return lambda x: x[0] + x[1]*len(schematic[0])


def get_moves(schematic, position, seen=None, diagonals=False, updown=False, adjacents=True):
    if seen is None:
        seen = set()

    x, y = position
    dxs = [dx for dx in [-1, 0, 1] if 0 <= x+dx < len(schematic[0])]
    if not updown:
        dys = [0,]
    else:
        dys = [dy for dy in [-1, 0, 1] if 0 <= y+dy < len(schematic)]

    moves = []
    for dx, dy in itertools.product(dxs, dys):
        if dx==dy==0:
            continue
        if (x+dx, y+dy) in seen:
            continue
        if not diagonals and abs(dx) + abs(dy) > 1:
            continue
        if not adjacents and abs(dx) + abs(dy) == 1:
            continue
        moves.append((dx, dy))

    return moves


def explore_island(schematic, start):
    seen = set()
    island = set()
    pos_queue = [start,]

    while len(pos_queue):
        current = pos_queue.pop()
        seen.add(current)

        if not is_digit(schematic[current[1]][current[0]]):
            continue

        island.add(current)

        moves = get_moves(schematic, current, seen)
        for m in moves:
            pos_queue.append( (current[0]+m[0], current[1]+m[1]) )

    return island


def get_int_from_island(schematic, island):
    island = sorted(island, key=get_sort_key(schematic))
    nums = [schematic[p[1]][p[0]] for p in island]
    return int(''.join(nums))


def island_is_engine(schematic, island):
    for pos in island:
        moves = get_moves(schematic, pos, island, diagonals=True, updown=True)
        for move in moves:
            new_pos = (pos[0]+move[0], pos[1]+move[1])
            if schematic[new_pos[1]][new_pos[0]] != '.':
                return True
    return False


def add_all_engines(schematic):
    total = 0

    seen = set()
    for pos in itertools.product(range(len(schematic[0])), range(len(schematic[1]))):
        if pos in seen:
            continue
        seen.add(pos)

        if not is_digit(schematic[pos[1]][pos[0]]):
            continue

        island = explore_island(schematic, pos)
        [seen.add(p) for p in island]
        if island_is_engine(schematic, island):
            val = get_int_from_island(schematic, island)
            total += val

    return total


def find_all_symbol(schematic, symbol):
    star_positions = []
    for pos in itertools.product(range(len(schematic[0])), range(len(schematic[1]))):
        if schematic[pos[1]][pos[0]] == symbol:
            star_positions.append(pos)
    return star_positions


def get_gear_value(schematic, pos):
    if schematic[pos[1]][pos[0]] != '*':
        return 0

    islands = []
    moves = get_moves(schematic, pos, diagonals=True, updown=True)
    for m in moves:
        new_pos = (pos[0]+m[0], pos[1]+m[1])
        island = explore_island(schematic, new_pos)
        if len(island):
            islands.append(island)

    if len(islands) < 2:
        return 0

    unique_islands = []
    for island_a in islands:
        for island_b in unique_islands:
            if len(island_a.intersection(island_b)) != 0:
                break
        else:
            unique_islands.append(island_a)

    if len(unique_islands) != 2:
        return 0

    return get_int_from_island(schematic, unique_islands[0]) * get_int_from_island(schematic, unique_islands[1])


def main():
    schematic = load_file("data/day_03.txt")
    checksum_1 = add_all_engines(schematic)
    print(f"Part 1\n{checksum_1}")

    all_stars = find_all_symbol(schematic, '*')
    checksum_2 = sum((get_gear_value(schematic, p) for p in all_stars))
    print(f"Part 2\n{checksum_2}")


if __name__ == "__main__":
    main()