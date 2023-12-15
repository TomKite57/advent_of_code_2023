
from collections import defaultdict

def load_file(fname):
    with open(fname, 'r') as file:
        data = file.read().strip().split(',')
    return data

def hash(line):
    val = 0
    for char in line:
        val += ord(char)
        val *= 17
        val %= 256
    return val

def process_line(line, box_states):

    is_minus = bool(line.find('-') != -1)
    is_equal = bool(line.find('=') != -1)
    assert int(is_minus) + int(is_equal) == 1

    if is_minus:
        label = line.strip("-")
        line_hash = hash(label)
        to_remove = [i for i, box in enumerate(box_states[line_hash]) if box[0]==label]
        if len(to_remove) == 0:
            return
        box_states[line_hash].pop(to_remove[0])

    else:
        label, focal_length = line.split("=")
        line_hash = hash(label)
        label_in_box = [i for i, box in enumerate(box_states[line_hash]) if box[0]==label]
        if len(label_in_box) == 0:
            box_states[line_hash].append((label, int(focal_length)))
        else:
            box_states[line_hash][label_in_box[0]] = (label, int(focal_length))

def score_box(box_states):
    rval = 0
    for k, v in box_states.items():
        for i, (l, f) in enumerate(v):
            rval += (k+1)*(i+1)*f
    return rval

def get_checksum_2(lines):
    box_states = defaultdict(list)

    for line in lines:
        process_line(line, box_states)

    return score_box(box_states)

def main():
    data = load_file("data/day_15.txt")

    checksum_1 = sum((hash(l) for l in data))
    print(f"Part 1\n{checksum_1}")

    checksum_2 = get_checksum_2(data)
    print(f"Part 2\n{checksum_2}")

if __name__ == "__main__":
    main()