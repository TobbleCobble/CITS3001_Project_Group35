#This solution doesn't spot the Strongly Connected Components or "flocks" that need to
#be counted. Instead, it counts the "swans" as they are visited in a DFS, which will fail
#as the longest path must be between SCC's, not between individual nodes. It also uses a 
#shared visited array for the DFS, which will mark the first nodes visited as "visited" and
#if they are encountered later will not be added into the "longest gossip chain".
import sys
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
def dfs(swan):
    visited[swan] = True
    best = 0

    for nextswan in adj[swan]:
        if not visited[nextswan]:
            best = max(best, 1 + dfs(nextswan))

    return best

print(dfs(0))