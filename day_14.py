
from tqdm import tqdm
from collections import defaultdict

def load_file(fname):
    with open(fname, 'r') as file:
        data = [[x for x in line.strip()] for line in file]
    return data

def full_roll(data, dir):
    dx, dy = dir

    while True:
        something_moved = False

        for y, row in enumerate(data):
            for x, elem in enumerate(row):
                if elem != 'O':
                    continue

                nx = x + dx if 0 <= x + dx < len(row) else None
                ny = y + dy if 0 <= y + dy < len(data) else None

                if nx is None or ny is None:
                    continue

                if data[ny][nx] == ".":
                    data[ny][nx] = 'O'
                    data[y][x] = '.'
                    something_moved = True

        if not something_moved:
            break

    return data

def full_spin(data):
    data = full_roll(data, ( 0, -1))
    data = full_roll(data, (-1,  0))
    data = full_roll(data, ( 0,  1))
    data = full_roll(data, ( 1,  0))
    return data

def get_checksum_2(data, cycles):
    history = defaultdict(list)
    current_cycles = 0
    period = -1

    while current_cycles != cycles:
        state = tuple([tuple(row) for row in data])
        history[state].append(current_cycles)
        if period == -1 and len(history[state]) > 1:
            period = history[state][1] - history[state][0]

            cycles_to_go = cycles - current_cycles
            periods_can_skip = cycles_to_go // period
            current_cycles += periods_can_skip*period

        data = full_spin(data)

        current_cycles += 1

    return get_load(data)

def get_load(data):
    rval = 0

    for y, row in enumerate(data):
        for x, elem in enumerate(row):
            if elem == 'O':
                rval += len(data)-y

    return rval

def show_data(data):
    for row in data:
        for elem in row:
            print(elem, end='')
        print()


def main():
    data = load_file("data/day_14.txt")
    original_data = [[x for x in row] for row in data]

    data = full_roll(data, (0, -1))
    checksum_1 = get_load(data)
    print(f"Part 1\n{checksum_1}")

    checksum_2 = get_checksum_2(original_data, 1000000000)
    print(f"Part 2\n{checksum_2}")

if __name__ == "__main__":
    main()