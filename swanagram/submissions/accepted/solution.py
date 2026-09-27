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

#Finally, knowing that the greedily best choice is to always choose
#1 as the gossip power, we can just find the longest path from Swanerberg's
#SCC to any other SCC and print that result. Since, different flocks cannot form
#a directed cycle, the graph is acyclic. A memoised DFS (as per lecture) can therefore
#find the longest gossip chain.

def dfs_longest_path(adjlist, flock):

    memo = {}
    def dfs(u):
        if u in memo:
            return memo[u]
        
        best = 0

        for v in adjlist[u]:
            best = max(best, 1 + dfs(v))

        memo[u] = best
        return best

    return dfs(flock)


print(dfs_longest_path(adjscc, swans_flock[0]))


