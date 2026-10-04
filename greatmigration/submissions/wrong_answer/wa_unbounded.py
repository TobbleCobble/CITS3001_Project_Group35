import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    capacity = int(input_data[1])

    items = []
    idx = 2
    for _ in range(n):
        wi = int(input_data[idx])
        vi = int(input_data[idx + 1])
        items.append((wi, vi))
        idx += 2

    dpt = [0 for _ in range(capacity + 1)]

    for wi, vi in items:
        # False assumption: iterating forwards instead of backwards.
        # This allows the same plant to be consumed multiple times.
        for w in range(wi, len(dpt)):
            dpt[w] = max(dpt[w], dpt[w - wi] + vi)

    print(dpt[-1])

if __name__ == '__main__':
    solve()