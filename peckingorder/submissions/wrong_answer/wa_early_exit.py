#wa_early_exit.py
#initial thoughts: kahns with a uniqueness check, but "optimised" to stop the moment
#the ready queue has 2+ swans since the answer cant be a single ranking any more
#false assumption: once its ambiguous its definitely AMBIGUOUS. a cycle later in the
#graph means there is NO ranking, so the answer should be CONTRADICTORY
#expected verdict: WRONG ANSWER when a log has both a choice point and a cycle
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
while ready:
    if len(ready) > 1:
        print("AMBIGUOUS")   #<-- too early, havent checked the rest for a cycle
        sys.exit(0)
    u = ready.popleft()
    order.append(u)
    for v in adj[u]:
        indeg[v] -= 1
        if indeg[v] == 0:
            ready.append(v)

if len(order) < n:
    print("CONTRADICTORY")
else:
    print(" ".join(map(str, order)))
