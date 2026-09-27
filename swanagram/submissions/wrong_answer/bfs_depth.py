#This solution runs Kosaraju's correctly, but then attempts to use BFS to find
#the longest path which fails because BFS is not guaranteed to find the longest path in
#a DAG. BFS marks a node visited the first time it's reached, corresponding to a shortest path.
#If the same node is later reachable through a longer path, BFS will ignore it, and fail to
#find the longest path.

from collections import deque
import sys
sys.setrecursionlimit(10**5)

N, M = map(int, input().split())

adj = [[] for _ in range(N)]

for edge in range(M):
    u, v = map(int, input().split())
    u-=1
    v-=1
    adj[u].append(v)

#To quickly find the "flock" of a swan, we will map each node to its SCC index
swans_flock = [-1]*N

#Kosaraju's Algorithm to find SCC's as in the lecture
def dfs_postorder(adjlist, visited, root):
    postorder = []
    def dfs(current):
        if not visited[current]:
            visited[current] = True
            for neighbor in adjlist[current]:
                dfs(neighbor)
            postorder.append(current)
    dfs(root)
    return postorder

def transpose(adjlist):
    result = [[] for _ in adjlist]
    for u in range(len(adjlist)):
        for v in adjlist[u]:
            result[v].append(u)
    return result

def kosarajus(adjlist):
    postorder = []
    visited = [False for _ in adjlist]
    for i in range(len(adjlist)):
        if not visited[i]:
            postorder.extend(dfs_postorder(adjlist, visited, i))

    transposed = transpose(adjlist)
    visited = [False for _ in transposed]
    flocks = []

    for node in reversed(postorder):
        if not visited[node]:
            component = dfs_postorder(transposed, visited, node)

            #Add the component to the list of SCC's and map each node to its SCC index
            #Used later for building the new adjacency list of SCC's
            flocks.append(component)
            for n in component:
                swans_flock[n] = len(flocks) - 1
    return flocks

#Need a new adjacency list for the SCC's
flocks = kosarajus(adj)

adjscc = [[] for _ in range(len(flocks))]

for swan in range(N):
    for swan2 in adj[swan]:
        if(swans_flock[swan] != swans_flock[swan2]):
            adjscc[swans_flock[swan]].append(swans_flock[swan2])

#Now, we incorrectly can use BFS to try to find the longest gossip chain

def bfs_longest_path(adjlist, flock):
    queue = deque([(flock, 0)])
    visited = [False for _ in adjlist]
    visited[flock] = True

    best = 0

    while queue:
        current, depth = queue.popleft()
        best = max(best, depth)

        for neighbor in adjlist[current]:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append((neighbor, depth + 1))

    return best

print(bfs_longest_path(adjscc, swans_flock[0]))
