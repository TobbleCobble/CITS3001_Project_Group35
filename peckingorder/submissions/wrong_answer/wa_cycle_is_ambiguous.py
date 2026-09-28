#wa_cycle_is_ambiguous.py
#initial thoughts: full kahns run, but lumps both failure cases together
#false assumption: a cycle means "the log cant decide", same as having many rankings.
#really a cycle means no ranking fits at all -> CONTRADICTORY
#expected verdict: WRONG ANSWER on every cyclic test (already fails sample 3)
import sys
from collections import deque

#read input in one go
def read_graph():
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for i in range(m):
        a = int(data[2 + 2 * i])
        b = int(data[3 + 2 * i])
        adj[a].append(b)
        indeg[b] += 1
    return n, adj, indeg

n, adj, indeg = read_graph()
ready = deque(v for v in range(1, n + 1) if indeg[v] == 0)
order = []
unique = True
while ready:
    if len(ready) > 1:
        unique = False
    u = ready.popleft()
    order.append(u)
    for v in adj[u]:
        indeg[v] -= 1
        if indeg[v] == 0:
            ready.append(v)

#<-- conflates "no ranking" with "many rankings"
if len(order) < n or not unique:
    print("AMBIGUOUS")
else:
    print(" ".join(map(str, order)))
