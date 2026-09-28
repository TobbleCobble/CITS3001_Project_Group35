"""
TIME LIMIT EXCEEDED - correct but exponential brute force.

It enumerates every way the swans could each pick one of their available
lunches (the Cartesian product of the swans' option lists, produced by
itertools.product -- an "odometer" that rolls each swan's choice like a digit).
For each combination it scores the number of DISTINCT lunches used, so two
swans landing on the same lunch never over-count, and the maximum over all
combinations is the true answer.

This is genuinely correct, but the number of combinations is the product of the
swans' option counts -- exponential -- so it cannot finish within the time limit
on the larger tests. Swans that fear every lunch are dropped (no options).
"""
from itertools import product


def main():
    S, L = map(int, input().split())

    options = []
    for _ in range(S):
        parts = list(map(int, input().split()))
        feared = set(parts[1:])
        opts = [lunch for lunch in range(1, L + 1) if lunch not in feared]
        if opts:                     # a swan that fears everything cannot steal
            options.append(opts)

    best = 0
    for combo in product(*options):          # every combination of swan choices
        best = max(best, len(set(combo)))    # distinct lunches actually used
    print(best)


main()
