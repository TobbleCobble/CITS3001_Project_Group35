from itertools import product

def main():
    s, l = map(int, input().split())

    swanslunches = []
    for _ in range(s):
        parts = list(map(int, input().split()))
        feared = set(parts[1:])
        option = [lunch for lunch in range(1, l + 1) if lunch not in feared]
        if option:                     # a swan that fears everything cannot steal
            swanslunches.append(option)

    best = 0
    for combo in product(*swanslunches): # this product function givees you all the possible combinations of lunches and swans
        best = max(best, len(set(combo))) # take the max combination of lunches stolen by swans in the list of allocations
    print(best)

main()
