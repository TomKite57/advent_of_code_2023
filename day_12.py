
from collections import defaultdict
from tqdm import tqdm

def parse_line(line):
    springs, nums = line.strip().split(' ')
    nums = [int(x) for x in nums.split(',')]
    return [springs, nums]

def load_file(fname):
    with open(fname, 'r') as file:
        data = [parse_line(l) for l in file]
    return data

def count_groups(springs):
    counts = []
    running_counter = 0

    for char in springs:
        if char == '#':
            running_counter += 1
        elif char == '.':
            if running_counter != 0:
                counts.append(running_counter)
            running_counter = 0

    if running_counter != 0:
        counts.append(running_counter)

    return counts

def count_closed(springs):
    counts = []
    running_counter = 0

    for char in springs:
        if char == '#':
            running_counter += 1
        elif char == '.':
            if running_counter != 0:
                counts.append(running_counter)
            running_counter = 0
        elif char == '?':
            break

    return counts, running_counter


def count_valid_constructions(springs, nums):
    first_missing = springs.find('?')
    if first_missing == -1:
        return 1 if count_groups(springs) == nums else 0

    rval = 0

    spaces = springs.count('?')
    hash_to_place = sum(nums) - springs.count('#')

    if hash_to_place > spaces:
        return rval

    a = "".join([s if i != first_missing else '#' for i, s in enumerate(springs)])
    b = "".join([s if i != first_missing else '.' for i, s in enumerate(springs)])

    # Stop early?
    early_a_nums, current = count_closed(a)
    if early_a_nums == nums and current == 0:
        rval += 1
    elif 0 < hash_to_place and all([x==y for x, y in zip(early_a_nums, nums)]) and (current == 0 or current <= nums[len(early_a_nums)]):
        rval += count_valid_constructions(a, nums)

    early_b_nums, current = count_closed(b)
    if early_b_nums == nums and current == 0:
        rval += 1
    elif all([x==y for x, y in zip(early_b_nums, nums)]) and (current == 0 or current <= nums[len(early_b_nums)]):
        rval += count_valid_constructions(b, nums)

    return rval

def build_all_constructions(springs):
    rval = defaultdict(int)

    first_missing = springs.find('?')
    if first_missing == -1:
        rval[tuple(count_groups(springs))] += 1
        return rval

    a = "".join([s if i != first_missing else '#' for i, s in enumerate(springs)])
    b = "".join([s if i != first_missing else '.' for i, s in enumerate(springs)])

    arval = build_all_constructions(a)
    brval = build_all_constructions(b)
    for k, v in arval.items():
        rval[k] += v
    for k, v in brval.items():
        rval[k] += v

    return rval

def get_action_groups(springs):
    groups = []
    running = []

    for char in springs:
        if char == '.':
            groups.append(running)
            running = []
        else:
            running.append(char)
    groups.append(running)

    return [''.join(r) for r in groups if len(r)>0]

def expand_springs(springs, nums):
    springs = "?".join([springs]*5)
    nums = nums*5
    return springs, nums

def main():
    data = load_file("data/day_12.txt")

    #for springs, nums in data:
    #    print(springs, nums, count_valid_constructions(springs, nums))

    checksum_1 = sum((count_valid_constructions(springs, nums) for springs, nums in data))
    print(f"Part 1\n{checksum_1}")

    #all_action_groups = dict()
    #for line, nums in data:
    #    line, nums = expand_springs(line, nums)
    #    for g in get_action_groups(line):
    #        if g in all_action_groups:
    #            continue
    #        all_action_groups[g] = build_all_constructions(g)
#
    #for k, v in all_action_groups.items():
    #    print(k, v)

    checksum_2 = 0
    for springs, nums in tqdm(data):
        checksum_2 += count_valid_constructions(*expand_springs(springs, nums))
    print(f"Part 2\n{checksum_2}")


if __name__ == "__main__":
    main()