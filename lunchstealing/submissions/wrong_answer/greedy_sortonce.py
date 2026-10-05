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

    # sort lunches once, fewest possible swans first
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
