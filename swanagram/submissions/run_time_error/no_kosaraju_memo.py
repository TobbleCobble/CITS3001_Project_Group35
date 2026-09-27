#This solution doesn't spot the Strongly Connected Components or "flocks" that need to
#be counted. Instead, it counts the "swans" as they are visited in a DFS, which will fail
#as the longest path must be between SCC's, not between individual nodes. However, it also
#doesn't spot the potential for cycles in the graph, and so will run into a RecursionError
#by attempting to run a memoised DFS on a graph with cycles. 
import sys
from functools import cache
sys.setrecursionlimit(10**5)

N, M = map(int, input().split())

adj = [[] for _ in range(N)]

for edge in range(M):
    u, v = map(int, input().split())
    u-=1
    v-=1
    adj[u].append(v)

visited = [False]*N

#Run a DFS to find the longest path from Swanerberg's node (0) to any other node in the graph.
@cache
def dfs(swan):
    best = 0

    for nextswan in adj[swan]:
        best = max(best, 1 + dfs(nextswan))

    return best

print(dfs(0))