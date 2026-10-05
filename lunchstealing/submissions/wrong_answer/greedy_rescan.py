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

    used_swans = set()      # swans already assigned a lunch
    taken_lunches = set()   # lunches already stolen
    stolen = 0

    while True:
        # find the lunch with the fewest swans and pair them up
        best_lunch = None
        best_available = None
        for lunch in range(1, L + 1):
            if lunch in taken_lunches:
                continue
            available = can[lunch] - used_swans # this is what does the rescan
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
