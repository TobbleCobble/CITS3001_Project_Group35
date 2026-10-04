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

    def recurrence(i, w):
        # Base case: out of items or out of capacity
        if i == 0 or w == 0:
            return 0

        wi, vi = items[i - 1]

        # If the item doesn't fit, we must skip it
        if w < wi:
            return recurrence(i - 1, w)
        # Otherwise, take the max of skipping it or taking it
        else:
            return max(
                recurrence(i - 1, w),
                recurrence(i - 1, w - wi) + vi
            )

    print(recurrence(n, capacity))

if __name__ == '__main__':
    sys.setrecursionlimit(2000)  # Prevents Python from crashing before the TLE
    solve()