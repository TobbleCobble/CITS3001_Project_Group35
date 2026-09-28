"""
WRONG ANSWER - a "clever" greedy that is still wrong.

Each round it fills the most-constrained lunch first: it looks at every
un-taken lunch, counts how many still-free swans could take it, and assigns a
swan to the lunch with the fewest options (re-evaluating after every choice).

This is a strong heuristic, but it never undoes an assignment. Maximum matching
sometimes needs an augmenting-path reroute -- moving an already-placed swan to
a different lunch so another swan can eat -- which greedy cannot do. So on the
hardest instances it strands a swan and reports fewer steals than the true
maximum. Fast (polynomial), so it fails as Wrong Answer, not Time Limit.
"""


def main():
    S, L = map(int, input().split())

    # can[lunch] = set of swans that can steal that lunch (not scared of it)
    can = {j: set() for j in range(1, L + 1)}
    for _ in range(S):
        parts = list(map(int, input().split()))
        swan = parts[0]
        feared = set(parts[1:])
        for lunch in range(1, L + 1):
            if lunch not in feared:
                can[lunch].add(swan)

    used_swans = set()      # swans already assigned a lunch
    taken_lunches = set()   # lunches already stolen
    stolen = 0

    while True:
        # find the un-taken lunch with the fewest STILL-FREE swans
        best_lunch = None
        best_available = None
        for lunch in range(1, L + 1):
            if lunch in taken_lunches:
                continue
            available = can[lunch] - used_swans
            if not available:
                continue
            if best_lunch is None or len(available) < len(best_available):
                best_lunch = lunch
                best_available = available

        if best_lunch is None:      # nothing else can be assigned
            break

        used_swans.add(min(best_available))   # assign one free swan
        taken_lunches.add(best_lunch)
        stolen += 1

    print(stolen)


main()
