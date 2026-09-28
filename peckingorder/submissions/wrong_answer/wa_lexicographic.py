#wa_lexicographic.py
#initial thoughts: kahns algorithm with a min-heap, gives the lexicographically smallest
#topological order - a standard exercise, so easy to reach for by habit
#false assumption: any valid ranking is the answer. it always prints SOME order when the
#log is acyclic, so it never says AMBIGUOUS
#expected verdict: WRONG ANSWER on every ambiguous test
import sys
import heapq

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
#heap instead of a queue so the smallest ready swan always goes next
ready = [v for v in range(1, n + 1) if indeg[v] == 0]
heapq.heapify(ready)
order = []
while ready:
    u = heapq.heappop(ready)   #<-- picks one when there might be a choice, never flags it
    order.append(u)
    for v in adj[u]:
        indeg[v] -= 1
        if indeg[v] == 0:
            heapq.heappush(ready, v)

if len(order) < n:
    print("CONTRADICTORY")
else:
    print(" ".join(map(str, order)))
