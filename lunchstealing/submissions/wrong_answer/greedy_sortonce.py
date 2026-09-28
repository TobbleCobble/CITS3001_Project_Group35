"""
WRONG ANSWER - a cruder greedy than greedy_rescan.py.

It ranks the lunches once, by how many swans could take each at the START, and
fills the most-contested first in that fixed order. It never updates the counts
as swans get used, and never reconsiders a choice. Because it works from stale
information, it strands swans on more instances than the re-evaluating version
does -- so it is wrong on more of the tests. Still polynomial, so Wrong Answer,
not Time Limit.
"""


def main():
    S, L = map(int, input().split())

    # can[lunch] = set of swans that can steal that lunch
    can = {j: set() for j in range(1, L + 1)}
    for _ in range(S):
        parts = list(map(int, input().split()))
        swan = parts[0]
        feared = set(parts[1:])
        for lunch in range(1, L + 1):
            if lunch not in feared:
                can[lunch].add(swan)

    # sort lunches once, fewest possible swans first (static counts)
    order = sorted(range(1, L + 1), key=lambda lunch: len(can[lunch]))

    used_swans = set()
    stolen = 0
    for lunch in order:
        free = can[lunch] - used_swans      # swans that can take it and are unused
        if free:
            used_swans.add(min(free))
            stolen += 1

    print(stolen)


main()
