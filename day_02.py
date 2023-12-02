
TOTALS = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

COLORS = set(TOTALS.keys())

def parse_line(line):
    _id, rest = line.strip().split(": ")
    _id = int(_id.strip("Game "))

    rounds = rest.split("; ")
    rounds = [r.split(", ") for r in rounds]
    rounds = [[b.split(' ') for b in balls] for balls in rounds]
    rounds = [{b: int(a) for a, b in balls} for balls in rounds]

    return _id, rounds


def parse_file(fname):
    with open(fname, 'r') as file:
        lines = [parse_line(line) for line in file]
    return lines


def valid_round(_round):
    for color, total in TOTALS.items():
        if _round.get(color, 0) > total:
            return False
    return True


def valid_game(game):
    for _round in game:
        if not valid_round(_round):
            return False
    return True


def total_product(arr):
    total = 1
    for x in arr:
        total *= x
    return total


def game_power(game):
    mins = {c: 0 for c in COLORS}
    for _round in game:
        mins = {c: max(mins[c], _round.get(c, 0)) for c in COLORS}

    return total_product(mins.values())


def main():
    all_games = parse_file("data/day_02.txt")
    checksum_1 = sum((_id for _id, game in all_games if valid_game(game)))
    print(f"Part 1\n{checksum_1}")

    checksum_2 = sum((game_power(game) for _, game in all_games))
    print(f"Part 2\n{checksum_2}")


if __name__ == "__main__":
    main()