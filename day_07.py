
CARDS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
CARDS_ORDER = {c: i for i, c in enumerate(CARDS)}
HANDS = ["five_kind", "four_kind", "full_house", "three_kind", "two_pair", "one_pair", "high_card"]
HANDS_ORDER = {h: i for i, h in enumerate(HANDS)}

P2_CARDS = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
P2_CARDS_ORDER = {c: i for i, c in enumerate(P2_CARDS)}


def load_file(fname):
    with open(fname, 'r') as file:
        lines = [l.strip().split(' ') for l in file]
    lines = [[a, int(b)] for a, b in lines]
    return lines

def get_hand_type(hand):
    unique_cards = set(hand)
    card_counts = {c: hand.count(c) for c in unique_cards}
    unique_counts = set(card_counts.values())

    if 5 in unique_counts:
        return "five_kind"
    if 4 in unique_counts:
        return "four_kind"
    if 3 in unique_counts:
        if 2 in unique_counts:
            return "full_house"
        return "three_kind"
    if 2 in unique_counts:
        if list(card_counts.values()).count(2) == 2:
            return "two_pair"
        return "one_pair"
    return "high_card"

def get_sort_score(hand):
    c_len = len(CARDS)

    score = HANDS_ORDER[get_hand_type(hand)]*c_len**5
    for i, c in enumerate(hand[::-1]):
        score += c_len**(i)*CARDS_ORDER[c]

    return score

def get_hand_type_p2(hand):
    unique_cards = set(hand)
    card_counts = {c: hand.count(c) for c in unique_cards}
    unique_counts = set(card_counts.values())

    if hand=="JJJJJ":
        return "five_kind"

    for i, c in enumerate(hand):
        if c == "J":
            max_count = max(card_counts.items(), key=lambda x: x[1] if x[0]!="J" else -1)
            if max_count[0] == "J":
                max_count = ("A", None)
            new_hand = "".join([x if j != i else max_count[0] for j, x in enumerate(hand)])
            return get_hand_type_p2(new_hand)

    if 5 in unique_counts:
        return "five_kind"
    if 4 in unique_counts:
        return "four_kind"
    if 3 in unique_counts:
        if 2 in unique_counts:
            return "full_house"
        return "three_kind"
    if 2 in unique_counts:
        if list(card_counts.values()).count(2) == 2:
            return "two_pair"
        return "one_pair"
    return "high_card"

def get_sort_score_p2(hand):
    c_len = len(CARDS)

    score = HANDS_ORDER[get_hand_type_p2(hand)]*c_len**5
    for i, c in enumerate(hand[::-1]):
        score += c_len**(i)*P2_CARDS_ORDER[c]

    return score


def main():
    data = load_file("data/day_07.txt")

    p1_data = sorted(data, key=lambda d: get_sort_score(d[0]), reverse=True)
    checksum_1 = sum(((i+1)*d[1] for i, d in enumerate(p1_data)))
    print(f"Part 1\n{checksum_1}")

    p2_data = sorted(data, key=lambda d: get_sort_score_p2(d[0]), reverse=True)
    checksum_2 = sum(((i+1)*d[1] for i, d in enumerate(p2_data)))
    print(f"Part 2\n{checksum_2}")

if __name__ == "__main__":
    main()