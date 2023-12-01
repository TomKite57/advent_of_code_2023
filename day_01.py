
STRING_TO_INT = {
    "one": '1',
    "two": '2',
    "three": '3',
    "four": '4',
    "five": '5',
    "six": '6',
    "seven": '7',
    "eight": '8',
    "nine": '9',
    "1": '1',
    "2": '2',
    "3": '3',
    "4": '4',
    "5": '5',
    "6": '6',
    "7": '7',
    "8": '8',
    "9": '9',
    }

def load_file(fname):
    with open(fname, 'r') as file:
        return [l.strip() for l in file]
    return lines


def is_digit(x):
    try:
        int(x)
        return True
    except ValueError as e:
        return False


def parse_ints_from_line(line):
    first, last = -1, -1

    for char in line:
        if is_digit(char):
            last = char
            if first == -1:
                first = char

    return first, last

def parse_ints_and_strings_from_line(line):
    words = list(STRING_TO_INT.keys())
    first_find = [line.find(w) for w in words]
    first_find = [x if x!=-1 else len(line)+1 for x in first_find]
    last_find = [line[::-1].find(w[::-1]) for w in words]
    last_find = [len(line) - len(w) - x if x!=-1 else -1 for x, w in zip(last_find, words)]

    first_ind_val = min(enumerate(first_find), key=lambda x: x[1])
    last_ind_val = max(enumerate(last_find), key=lambda x: x[1])

    first = STRING_TO_INT[words[first_ind_val[0]]]
    if last_ind_val[0] == -1:
        last = first
    else:
        last = STRING_TO_INT[words[last_ind_val[0]]]

    return first, last

def main():
    raw_lines = load_file("data/day_01.txt")
    parsed_ints_p1 = [parse_ints_from_line(l) for l in raw_lines]

    checksum_1 = sum((10*int(a) + int(b) for a, b in parsed_ints_p1))
    print(f"Part 1\n{checksum_1}")

    parsed_ints_p2 = [parse_ints_and_strings_from_line(l) for l in raw_lines]
    checksum_2 = sum((10*int(a) + int(b) for a, b in parsed_ints_p2))
    print(f"Part 2\n{checksum_2}")

if __name__ == "__main__":
    main()