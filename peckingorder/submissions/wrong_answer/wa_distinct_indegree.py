#wa_distinct_indegree.py
#initial thoughts: the log has duplicate entries, so count in-degree as the number of
#DISTINCT swans that beat each swan (using a set of predecessors)
#bug: the adjacency list still has every duplicate, so a swan gets decremented once per
#copy. eg 1 -> 3 logged twice drops 3s in-degree by 2 and it can go "ready" before
#another swan that also beats it has been placed
#expected verdict: WRONG ANSWER on tests with repeated entries into a swan with 2+ bosses
import sys
from collections import deque

#read input, in-degree from a set of predecessors (the mismatch)
def read_graph():
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]
    preds = [set() for _ in range(n + 1)]
    for i in range(m):
        a = int(data[2 + 2 * i])
        b = int(data[3 + 2 * i])
        adj[a].append(b)   #dupes kept here...
        preds[b].add(a)    #...but collapsed here
    indeg = [len(preds[v]) for v in range(n + 1)]
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
        indeg[v] -= 1   #<-- once per copy, so can hit 0 too early
        if indeg[v] == 0:
            ready.append(v)

if len(order) < n:
    print("CONTRADICTORY")
elif not unique:
    print("AMBIGUOUS")
else:
    print(" ".join(map(str, order)))
