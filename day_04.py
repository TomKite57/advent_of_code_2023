
def parse_line(line):
    card_num, nums = line.strip().split(': ')
    card_num = int(card_num.lstrip("Card "))

    winning, mine = nums.split(" | ")
    winning = [int(x) for x in winning.split(' ') if len(x)]
    mine = [int(x) for x in mine.split(' ') if len(x)]
    return card_num, winning, mine


def load_file(fname):
    with open(fname, 'r') as file:
        data = [parse_line(line) for line in file]
    nums = [x[0] for x in data]
    wins = [x[1] for x in data]
    mine = [x[2] for x in data]
    return nums, wins, mine


def get_matches(win, mine):
    return len(set(win).intersection(set(mine)))


def card_score(win, mine):
    matches = get_matches(win, mine)
    score = 0 if matches==0 else 2**(matches-1)
    return score


def part_2(nums, winning, mine):
    multipliers = {n: 1 for n in nums}
    total_cards = 0

    for num_i, win_i, mine_i in zip(nums, winning, mine):
        mult = multipliers[num_i]
        total_cards += mult
        matches = get_matches(win_i, mine_i)
        for i in range(matches):
            multipliers[num_i + i + 1] += mult

    return total_cards


def main():
    nums, winning, mine = load_file("data/day_04.txt")

    checksum_1 = sum(card_score(a, b) for a, b in zip(winning, mine))
    print(f"Part 1\n{checksum_1}")

    checksum_2 = part_2(nums, winning, mine)
    print(f"Part 2\n{checksum_2}")


if __name__ == "__main__":
    main()