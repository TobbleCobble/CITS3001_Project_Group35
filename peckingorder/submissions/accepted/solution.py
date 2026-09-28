#solution.py
#initial thoughts: each log entry "a b" is a directed edge a -> b (a outranks b), so a
#ranking consistent with the log is exactly a topological order of this graph
#use kahns algorithm - repeatedly take a swan that nobody left in the pool outranks
#if the pool of ready swans ever holds 2+ swans, either could go next -> AMBIGUOUS
#if kahns stops before placing all n swans, whats left must contain a cycle -> CONTRADICTORY
#have to finish the whole run before reporting AMBIGUOUS, a cycle further down beats it
#duplicate entries are fine as long as we add AND remove each copy once from the in-degree
import sys
from collections import deque

#read the whole input in one go - input() per line is too slow for 2*10^5 lines
def read_graph():
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]   #adj[a] = swans that a outranks (dupes kept)
    indeg = [0] * (n + 1)              #indeg[b] = number of log entries saying someone beats b
    for i in range(m):
        a = int(data[2 + 2 * i])
        b = int(data[3 + 2 * i])
        adj[a].append(b)
        indeg[b] += 1
    return n, adj, indeg

#kahns algorithm, also tracks whether there was ever a choice of who goes next
def kahn_unique(n, adj, indeg):
    #start with every swan nobody outranks
    ready = deque(v for v in range(1, n + 1) if indeg[v] == 0)
    order = []
    unique = True
    while ready:
        if len(ready) > 1:
            unique = False   #2+ swans could be placed here, dont stop yet (might be a cycle later)
        u = ready.popleft()
        order.append(u)
        #u is placed, so remove each of its log entries
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                ready.append(v)
    return order, unique

n, adj, indeg = read_graph()
order, unique = kahn_unique(n, adj, indeg)

#check cycle first - no ranking at all beats "many rankings"
if len(order) < n:
    print("CONTRADICTORY")
elif not unique:
    print("AMBIGUOUS")
else:
    print(" ".join(map(str, order)))
