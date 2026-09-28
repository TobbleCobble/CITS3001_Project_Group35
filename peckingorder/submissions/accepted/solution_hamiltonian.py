#solution_hamiltonian.py
#initial thoughts: different way to check uniqueness than watching the queue size
#get ANY topological order first (kahns), if it doesnt cover all n swans theres a cycle
#then the order is forced iff every consecutive pair (order[i], order[i+1]) is an actual
#log entry, ie the dag has a hamiltonian path
#why: if some consecutive pair u, w has no edge u -> w then no path can go u ~> w either
#(anything between them would have to sit between them in the order), so swapping u and w
#gives a second valid ranking. if every pair is an edge the whole order is one long chain
#and nothing can move
import sys
from collections import deque

#read input, also keep a set of (a, b) entries for the consecutive pair lookups
def read_graph():
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    edges = set()   #dupes collapse here, which is fine - only need to know if the entry exists
    for i in range(m):
        a = int(data[2 + 2 * i])
        b = int(data[3 + 2 * i])
        adj[a].append(b)
        indeg[b] += 1
        edges.add((a, b))
    return n, adj, indeg, edges

#plain kahns, returns any topological order (short if theres a cycle)
def topo_order(n, adj, indeg):
    ready = deque(v for v in range(1, n + 1) if indeg[v] == 0)
    order = []
    while ready:
        u = ready.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                ready.append(v)
    return order

n, adj, indeg, edges = read_graph()
order = topo_order(n, adj, indeg)

if len(order) < n:
    print("CONTRADICTORY")
#every neighbouring pair in the order must be joined by a log entry
elif all((order[i], order[i + 1]) in edges for i in range(n - 1)):
    print(" ".join(map(str, order)))
else:
    print("AMBIGUOUS")
