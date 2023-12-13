
def load_file(fname):
    with open(fname, 'r') as file:
        data = [[x for x in row.strip()] for row in file]
    return data

def get_empty_rows_cols(space):
    rows = set(list(range(len(space))))
    cols = set(list(range(len(space[0]))))

    for y, row in enumerate(space):
        for x, elem in enumerate(row):
            if elem != ".":
                if x in cols:
                    cols.remove(x)
                if y in rows:
                    rows.remove(y)

    return rows, cols

def get_galaxy_positions(space):
    galaxies = set()

    for y, row in enumerate(space):
        for x, elem in enumerate(row):
            if elem != ".":
                galaxies.add((x, y))

    return galaxies

def get_expanded_length(space, pos_a, pos_b, empty_rows, empty_cols, fac):
    x, y = pos_a
    xx, yy = pos_b
    dx = 1 if xx > x else -1
    dy = 1 if yy > y else -1

    length = 0
    while x != xx:
        x += dx
        if x in empty_cols:
            length += fac
        else:
            length += 1

    while y != yy:
        y += dy
        if y in empty_rows:
            length += fac
        else:
            length += 1

    return length

def get_checksum_1(space, galaxies, empty_rows, empty_cols, fac=2):
    galaxy_list = list(galaxies)

    rval = 0
    for i, ga in enumerate(galaxy_list):
        for gb in galaxy_list[i+1:]:
            rval += get_expanded_length(space, ga, gb, empty_rows, empty_cols, fac)

    return rval


def main():
    space = load_file("data/day_11.txt")
    galaxies = get_galaxy_positions(space)
    empty_rows, empty_cols = get_empty_rows_cols(space)

    checksum_1 = get_checksum_1(space, galaxies, empty_rows, empty_cols)
    print(f"Part 1\n{checksum_1}")

    checksum_2 = get_checksum_1(space, galaxies, empty_rows, empty_cols, 1000000)
    print(f"Part 2\n{checksum_2}")


if __name__ == "__main__":
    main()