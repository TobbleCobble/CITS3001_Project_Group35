#This solution runs Kosaraju's correctly, and spots a potential Greedy Approach,
#but incorrectly interprets that the flock's Gossip Power implies that the longest
#path must be between the largest flocks. This isn't true, as Gossip Power doesn't
#imply that there is a longer path after the bigger flock, and so the solution will fail.

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

#A greedy DFS to find the longest path by always choosing the next flock with
#the "largest Gossip Power" (i.e. the largest flock). 

def greedy_dfs(flock):
    
    if not adjscc[flock]:
        return 0

    next_flock = 0
    for next_flock_candidate in adjscc[flock]:
        if len(flocks[next_flock_candidate]) > len(flocks[next_flock]):
            next_flock = next_flock_candidate


    return 1 + greedy_dfs(next_flock)

print(greedy_dfs(swans_flock[0]))