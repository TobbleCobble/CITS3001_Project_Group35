#tle_all_pairs.py
#initial thoughts: correct idea, too slow
#the ranking is forced exactly when every pair of swans is comparable (one reaches the other)
#in a dag each comparable pair gets counted exactly once if we add up how many swans
#each swan can reach, so the order is unique iff that total is n(n-1)/2
#problem: one graph search per swan is O(n(n+m)), around 4*10^10 steps at the limits
#expected verdict: TIME LIMIT EXCEEDED on the big chain tests
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

#plain kahns, only used to get an order and spot cycles
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

#count how many swans s can reach using an iterative dfs
def count_reachable(s, n, adj):
    seen = bytearray(n + 1)
    seen[s] = 1
    stack = [s]
    count = 0
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if not seen[v]:
                seen[v] = 1
                count += 1
                stack.append(v)
    return count

n, adj, indeg = read_graph()
order = topo_order(n, adj, indeg)

if len(order) < n:
    print("CONTRADICTORY")
else:
    #this loop is the quadratic part - one full search from every swan
    comparable = 0
    for s in range(1, n + 1):
        comparable += count_reachable(s, n, adj)
    if comparable == n * (n - 1) // 2:
        print(" ".join(map(str, order)))
    else:
        print("AMBIGUOUS")
