import sys
from fractions import Fraction

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

    # Sort by value to weight ratio, highest first
    items.sort(key=lambda x: Fraction(x[1], x[0]), reverse=True)

    weight = 0
    result = 0
    for wi, vi in items:
        # If the whole plant fits, eat it
        if weight + wi <= capacity:
            weight += wi
            result += vi
        # False assumption: stopping completely if the next best plant doesn't fit,
        # ignoring smaller plants that might still fit in the remaining capacity.

    print(result)

if __name__ == '__main__':
    solve()