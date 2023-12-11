
def load_file(fname):
    with open(fname, 'r') as file:
        rval = [[int(x) for x in l.strip().split(' ')] for l in file]
    return rval

def diff(arr):
    return [b-a for a, b in zip(arr[:-1], arr[1:])]

def extrapolate_arr(arr):
    diffs = [arr, ]
    while True:
        if all([x==0 for x in diffs[-1]]):
            break

        diffs.append(diff(diffs[-1]))

    rval = 0
    for d in diffs[::-1]:
        rval = d[-1] + rval
    return rval

def extrapolate_arr_back(arr):
    diffs = [arr, ]
    while True:
        if all([x==0 for x in diffs[-1]]):
            break

        diffs.append(diff(diffs[-1]))

    rval = 0
    for d in diffs[::-1]:
        rval = d[0] - rval
    return rval

def main():
    var_histories = load_file("data/day_09.txt")

    checksum_1 = sum((extrapolate_arr(arr) for arr in var_histories))
    print(f"Part 1\n{checksum_1}")

    checksum_2 = sum((extrapolate_arr_back(arr) for arr in var_histories))
    print(f"Part 2\n{checksum_2}")

if __name__ == "__main__":
    main()