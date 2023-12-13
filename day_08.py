
from collections import defaultdict

def load_file(fname):
    with open(fname, 'r') as file:
        raw_text = file.read().strip()
    instruc, graph = raw_text.split("\n\n")
    graph = graph.split("\n")
    graph = {
        g.split(" = ")[0]: tuple(g.split(" = ")[1].strip("(").strip(")").split(", ")) for g in graph
    }

    return instruc, graph

def follow_path(instruc, graph):
    pos = "AAA"
    counter = 0

    while pos != "ZZZ":
        direc = instruc[counter%len(instruc)]
        ind = 0 if direc=="L" else 1
        pos = graph[pos][ind]
        counter += 1

    return counter

def has_a_loop(history):
    for s, h in history.items():
        if len(h) > 1:
            return True
    return False

# Define a function to calculate the greatest common divisor (GCD) using Euclidean algorithm
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Define a function to calculate the LCM using the GCD
def lcm(*args):
    if len(args) < 2:
        raise ValueError("At least two arguments are required to calculate LCM.")

    result = args[0]

    for num in args[1:]:
        result = (result * num) // gcd(result, num)

    return result

def follow_multiple_paths(instruc, graph):
    counter = 0
    paths = [pos for pos in graph.keys() if pos[-1]=="A"]
    start = [(pos, counter%len(instruc)) for pos in paths]
    histories = [defaultdict(list) for _ in paths]
    [histories[i][(pos, counter%len(instruc))].append(counter) for i, pos in enumerate(paths)]

    while True:
        direc = instruc[counter%len(instruc)]
        ind = 0 if direc=="L" else 1
        paths = [graph[pos][ind] for pos in paths]
        counter += 1

        for i, p in enumerate(paths):
            histories[i][(p, counter%len(instruc))].append(counter)

        if all([has_a_loop(h) for h in histories]):
            break


    periods = []
    for his in histories:
        for (loc, instruc), times in his.items():
            if len(times) > 1:
                periods.append(times[1]-times[0])
                break

    first = []
    # All histories have cycle now
    for his in histories:
        for (loc, instruc), times in his.items():
            if loc[-1] == 'Z':
                first.append(times[0])

    return lcm(*periods)


def main():
    instruc, graph = load_file("data/day_08.txt")

    checksum_1 = follow_path(instruc, graph)
    print(f"Part 1\n{checksum_1}")

    checksum_2 = follow_multiple_paths(instruc, graph)
    print(f"Part 2\n{checksum_2}")

if __name__ == "__main__":
    main()