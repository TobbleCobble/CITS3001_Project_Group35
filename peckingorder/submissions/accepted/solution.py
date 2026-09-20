"""Reference solution: Kahn's algorithm with a uniqueness check."""
import sys
from collections import deque

def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    adj = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    p = 2
    for _ in range(m):
        a = int(data[p]); b = int(data[p + 1]); p += 2
        adj[a].append(b)
        indeg[b] += 1

    q = deque(v for v in range(1, n + 1) if indeg[v] == 0)
    order = []
    unique = True
    while q:
        if len(q) > 1:
            unique = False          # a choice existed at this step
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    if len(order) < n:
        print("CONTRADICTORY")      # cycle: no ranking is consistent
    elif not unique:
        print("AMBIGUOUS")
    else:
        sys.stdout.write(" ".join(map(str, order)) + "\n")

main()
