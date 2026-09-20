# CORRECT but too slow.
#
# The characterisation used here is sound: the ranking is forced exactly when
# every pair of swans is comparable (one reaches the other).  In a DAG each
# comparable pair is counted exactly once by summing |descendants(s)| over all
# s, so the order is unique iff that total is n(n-1)/2.
#
# The flaw is purely computational: one traversal per swan is Theta(N(N+M)),
# which is ~4x slower for every doubling of N and hopeless at N = 2*10^5.
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
        adj[a].append(b); indeg[b] += 1

    q = deque(v for v in range(1, n + 1) if indeg[v] == 0)
    order = []
    while q:
        u = q.popleft(); order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0: q.append(v)
    if len(order) < n:
        print("CONTRADICTORY"); return

    comparable = 0
    for s in range(1, n + 1):                    # <-- the quadratic part
        seen = bytearray(n + 1); seen[s] = 1
        st = [s]
        while st:
            u = st.pop()
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = 1; comparable += 1; st.append(v)
    if comparable != n * (n - 1) // 2:
        print("AMBIGUOUS")
    else:
        sys.stdout.write(" ".join(map(str, order)) + "\n")

main()
