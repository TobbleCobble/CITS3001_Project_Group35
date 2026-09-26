import sys

def solve():
    # Read all input from standard input
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    # Parse N (number of plants) and W (stomach capacity)
    n = int(input_data[0])
    capacity = int(input_data[1])

    # Parse the items: (volume, nutritional value)
    items = []
    idx = 2
    for _ in range(n):
        wi = int(input_data[idx])
        vi = int(input_data[idx + 1])
        items.append((wi, vi))
        idx += 2

    dpt = [0 for _ in range(capacity + 1)]

    for wi, vi in items:
        for w in reversed(range(wi, len(dpt))):
            dpt[w] = max(dpt[w], dpt[w - wi] + vi)

    # Write exactly the final integer to standard output
    print(dpt[-1])

if __name__ == '__main__':
    solve()