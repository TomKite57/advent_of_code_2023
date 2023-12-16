

from collections import defaultdict

coord_map = {
    'n': ( 0, -1),
    'e': ( 1,  0),
    's': ( 0,  1),
    'w': (-1,  0),
}

def load_file(fname):
    with open(fname, 'r') as file:
        data = [row.strip() for row in file]
    return data

def show_map(data, history):
    for y, row in enumerate(data):
        for x, elem in enumerate(row):
            count = len(history[(x,y)]) if (x, y) in history else 0
            if count == 0:
                print(elem, end='')
            elif count == 1:
                print('#', end='')
            else:
                print(count, end='')
        print()


def trace_beams(data, *, start=(-1, 0, 'e'), return_count=False):
    beams = [start,]
    history = defaultdict(set)

    while len(beams):
        current_beam = beams.pop()
        x, y, direc = current_beam
        dx, dy = coord_map[direc]
        nx, ny = x+dx, y+dy

        if direc in history[(x, y)]:
            continue

        history[(x, y)].add(direc)

        if (not 0 <= nx < len(data[0])) or (not 0 <= ny < len(data)):
            continue

        next_tile = data[ny][nx]

        if next_tile == '.':
            beams.append((nx, ny, direc))
        elif next_tile == '/':
            new_direc = {'n': 'e', 'e': 'n', 's': 'w', 'w': 's'}
            beams.append((nx, ny, new_direc[direc]))
        elif next_tile == '\\':
            new_direc = {'n': 'w', 'e': 's', 's': 'e', 'w': 'n'}
            beams.append((nx, ny, new_direc[direc]))
        elif next_tile == '|':
            if direc in ['n', 's']:
                beams.append((nx, ny, direc))
            else:
                beams.append((nx, ny, 'n'))
                beams.append((nx, ny, 's'))
        elif next_tile == '-':
            if direc in ['e', 'w']:
                beams.append((nx, ny, direc))
            else:
                beams.append((nx, ny, 'e'))
                beams.append((nx, ny, 'w'))

    if return_count:
        return count_energised(data, history)

    return history


def count_energised(data, history):
    count = 0
    for k, v in history.items():
        x, y = k
        if 0 <= x < len(data[0]) and 0 <= y < len(data):
            count += 1
    return count


def max_energy_scan(data):
    max_val = 0
    for y in range(len(data)):
        max_val = max(max_val, trace_beams(data, start=(-1, y, 'e'), return_count=True))
        max_val = max(max_val, trace_beams(data, start=(len(data[0]), y, 'w'), return_count=True))
    for x in range(len(data[0])):
        max_val = max(max_val, trace_beams(data, start=(x, -1, 's'), return_count=True))
        max_val = max(max_val, trace_beams(data, start=(x, len(data), 'n'), return_count=True))

    return max_val


def main():
    data = load_file("data/day_16.txt")
    beam_history = trace_beams(data)

    #show_map(data, beam_history)

    checksum_1 = count_energised(data, beam_history)
    print(f"Part 1\n{checksum_1}")

    checksum_2 = max_energy_scan(data)
    print(f"Part 2\n{checksum_2}")

if __name__ == "__main__":
    main()