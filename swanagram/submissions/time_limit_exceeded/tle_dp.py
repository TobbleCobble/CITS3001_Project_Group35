#This solution doesn't spot the Greedy Approach to the problem, and
#instead tries to use dp for different "gossip powers" to find the longest path
#which would run in O(N^2) time, which is too slow for the problem constraints.
import sys
sys.setrecursionlimit(10**6)

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

#Finally, attempt to use dp to find the longest path from Swanerberg's SCC to
#another SCC

memo = {}

def dp(flock, gossip_power):
    best = 0
    if (flock, gossip_power) in memo:
        return memo[(flock, gossip_power)]
    
    for next_flock in adjscc[flock]:

        #We either go immediately to the next flock and stop there
        best = max(best, 1 + dp(next_flock, len(flocks[next_flock])))

        #Or we use this flock as a relay and continue the gossip with a
        #reduced gossip power
        if(gossip_power > 1):
            best = max(best, dp(next_flock, gossip_power - 1))

    memo[(flock, gossip_power)] = best
    return best


print(dp(swans_flock[0], len(flocks[swans_flock[0]])))
