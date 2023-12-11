
def load_file(fname):
    with open(fname, 'r') as file:
        line1, line2 = file.readlines()
    line1 = [int(x) for x in line1.strip().strip('Time:').split()]
    line2 = [int(x) for x in line2.strip().strip('Distance:').split()]
    return line1, line2

def get_distance(time_limit, charge):
    return charge*(time_limit-charge)

def get_wins(time_limit, distance):
    return sum((1 for i in range(time_limit) if get_distance(time_limit, i)>distance))

def prod(arr):
    total = 1
    for a in arr:
        total *= a
    return total

def main():
    time, distance = load_file("data/day_06.txt")

    checksum_1 = prod([get_wins(t, d) for t, d in zip(time, distance)])
    print(f"Part 1\n{checksum_1}")

    full_time = int(''.join([str(t) for t in time]))
    full_dist = int(''.join([str(d) for d in distance]))

    checksum_2 = get_wins(full_time, full_dist)
    print(f"Part 2\n{checksum_2}")

if __name__ == "__main__":
    main()