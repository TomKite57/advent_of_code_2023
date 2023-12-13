
from collections import defaultdict

def load_file(fname):
    with open(fname, 'r') as file:
        raw_data = file.read()
    segments = raw_data.split("\n\n")
    segments = [s.strip().split('\n') for s in segments]
    return segments

def get_segment_summary(segment):
    rows, cols = defaultdict(set), defaultdict(set)

    for y, row in enumerate(segment):
        for x, char in enumerate(row):
            if char == '#':
                rows[y].add(x)
                cols[x].add(y)

    return rows, cols

def find_vert_mirror(segment, cols):
    for i in range(0, len(segment[0])-1):
        has_vert = True
        for j in range(len(segment[0])):
            lj, rj = i-j, i+j+1

            if lj < 0 or rj >= len(segment[0]):
                break

            if cols[lj] != cols[rj]:
                has_vert = False
                break

        if has_vert:
            return i
    return -1

def find_hor_mirror(segment, rows):
    for i in range(0, len(segment)-1):
        has_hor = True
        for j in range(len(segment)):
            lj, rj = i-j, i+j+1

            if lj < 0 or rj >= len(segment):
                break

            if rows[lj] != rows[rj]:
                has_hor = False
                break

        if has_hor:
            return i
    return -1


def get_smudge_vert_reflection(segment, cols):
    for i in range(0, len(segment[0])-1):
        total_diff = 0
        for j in range(len(segment[0])):
            lj, rj = i-j, i+j+1

            if lj < 0 or rj >= len(segment[0]):
                break

            total_diff += len(cols[lj].union(cols[rj]) - cols[lj].intersection(cols[rj]))
            if total_diff > 1:
                break

        if total_diff == 1:
            return i
    return -1


def get_smudge_hor_reflection(segment, rows):
    for i in range(0, len(segment)-1):
        total_diff = 0
        for j in range(len(segment)):
            lj, rj = i-j, i+j+1

            if lj < 0 or rj >= len(segment):
                break

            total_diff += len(rows[lj].union(rows[rj]) - rows[lj].intersection(rows[rj]))
            if total_diff > 1:
                break

        if total_diff == 1:
            return i
    return -1

def get_checksum_1(data):
    checksum_1 = 0
    for i, seg in enumerate(data):
        rows, cols = get_segment_summary(seg)
        vert = find_vert_mirror(seg, cols)
        hor = find_hor_mirror(seg, rows)
        if hor == vert == -1 or (hor != -1 and vert != -1):
            print(i, hor, vert)

        if vert != -1:
            checksum_1 += vert+1
        if hor != -1:
            checksum_1 += (hor+1)*100
    return checksum_1


def get_checksum_2(data):
    checksum_2 = 0
    for i, seg in enumerate(data):
        rows, cols = get_segment_summary(seg)
        vert = find_vert_mirror(seg, cols)
        hor = find_hor_mirror(seg, rows)

        new_vert = get_smudge_vert_reflection(seg, cols)
        new_hor = get_smudge_hor_reflection(seg, rows)

        if new_vert != -1:
            checksum_2 += new_vert+1
        if new_hor != -1:
            checksum_2 += (new_hor+1)*100
    return checksum_2

def main():
    data = load_file("data/day_13.txt")

    checksum_1 = get_checksum_1(data)
    print(f"Part 1\n{checksum_1}")

    checksum_2 = get_checksum_2(data)
    print(f"Part 2\n{checksum_2}")

if __name__ == "__main__":
    main()