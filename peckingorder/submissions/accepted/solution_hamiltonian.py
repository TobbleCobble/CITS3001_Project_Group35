"""Alternative: produce ANY topological order, then verify consecutive pairs
are joined by an edge (unique order <=> the DAG has a Hamiltonian path)."""
import sys
from collections import deque

def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    adj = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    edges = set()
    p = 2
    for _ in range(m):
        a = int(data[p]); b = int(data[p + 1]); p += 2
        adj[a].append(b); indeg[b] += 1
        edges.add((a, b))

    q = deque(v for v in range(1, n + 1) if indeg[v] == 0)
    order = []
    while q:
        u = q.popleft(); order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    if len(order) < n:
        print("CONTRADICTORY"); return
    for i in range(n - 1):
        if (order[i], order[i + 1]) not in edges:
            print("AMBIGUOUS"); return
    sys.stdout.write(" ".join(map(str, order)) + "\n")

main()
