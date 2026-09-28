#rte_recursive_dfs.py
#initial thoughts: textbook dfs topological sort - reverse postorder is a topological order
#grey (on the stack) neighbour means a back edge -> cycle -> CONTRADICTORY
#then check consecutive pairs are log entries like the hamiltonian solution
#the logic is right but the dfs is recursive, and a chain of 2*10^5 swans goes 2*10^5 calls
#deep - way past pythons default recursion limit of 1000
#expected verdict: RUN TIME ERROR (RecursionError) on the long chain tests
import sys

#read input, keep an edge set for the final check
def read_graph():
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]
    edges = set()
    for i in range(m):
        a = int(data[2 + 2 * i])
        b = int(data[3 + 2 * i])
        adj[a].append(b)
        edges.add((a, b))
    return n, adj, edges

class CycleFound(Exception):
    pass

#recursive dfs, state 0 = unseen, 1 = on the current path, 2 = finished
def dfs(u, adj, state, post):
    state[u] = 1
    for v in adj[u]:
        if state[v] == 1:
            raise CycleFound()   #back edge
        if state[v] == 0:
            dfs(v, adj, state, post)   #<-- the recursion that blows up on a deep chain
    state[u] = 2
    post.append(u)

n, adj, edges = read_graph()
state = [0] * (n + 1)
post = []
try:
    for s in range(1, n + 1):
        if state[s] == 0:
            dfs(s, adj, state, post)
except CycleFound:
    print("CONTRADICTORY")
    sys.exit(0)

#reverse postorder = topological order
order = post[::-1]
if all((order[i], order[i + 1]) in edges for i in range(n - 1)):
    print(" ".join(map(str, order)))
else:
    print("AMBIGUOUS")
