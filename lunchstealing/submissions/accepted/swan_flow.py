from math import inf

#the ford fulkerson implemenation is very cloesly based off the lecture slides, with my own comments added

def ford_fulkerson(caps, s, t):

    # make sure every edge has a reverse partner with capacity 0 for the residual graph so we can add the back flow later

    for u in caps:
        for v in caps[u]:
            if u not in caps[v]:
                caps[v][u] = 0
    flows = {u: {v: 0 for v in caps[u]} for u in caps}
    total = 0
    while True:
        path = find_augmenting_path(caps, flows, s, t)
        if path is None:          # no augmenting path left -> current flow is maximum
            break
        total += push_flow(caps, flows, path)

    return total


def find_augmenting_path(caps, flows, s, t):
    # dfs through the residual graph if it still has has capacity
    parents = {}
    stack = [(s, s)]
    while stack:
        #stack implementation of dfs, top of the stack = most recently visited. we exhaust its neighbors before backtracking
        p, u = stack.pop()
        parents[u] = p
        for v in caps[u]:
            if v not in parents and flows[u][v] < caps[u][v]:
                stack.append((u, v))
    if t not in parents:
        #if sink not in the dfs / no augmenting path found
        return None
    path = [t]
    while path[-1] != s:
        path.append(parents[path[-1]])
        #rebuilding the dfs path and returning it in intiial order
    path.reverse()
    return path


def push_flow(caps, flows, path):
    # bottleneck = smallest remaining capacity along the path
    bottleneck = inf
    # base case for loop, first edge considered will always become bottleneck
    for u, v in zip(path, path[1:]):
        bottleneck = min(bottleneck, caps[u][v] - flows[u][v])
    # so the bottleneck is either the bottleneck of a previous edge, or the capacity of the current edge - flow pushed throgh it
    for u, v in zip(path, path[1:]):
        flows[u][v] += bottleneck #flow going through edge increased by bottleneck
        flows[v][u] -= bottleneck #reverse edge is updated for the flow that can now go back using it
    return bottleneck


def main():
    s, l = map(int, input().split())   # swans, lunches
    n = s + l + 2
    src, sink = 0, n - 1               # node 0 = source, node n-1 = sink

    
    # create a nested dictionary to represent edges and capacities
    caps = {u: {} for u in range(n)}   # one empty dict per node
    for swan in range(1, s + 1): # set all sink to swan edges to 1
        caps[src][swan] = 1
    for swan in range(1, s + 1):
        for lunch in range(1, l + 1):
            caps[swan][s + lunch] = 1  # nested loop to set all swan to lunch edges to 1
    for lunch in range(1, l + 1):
        caps[s + lunch][sink] = 1 #set all lunch to sink edges to 1

    # now we are removing the edges from swans if they fear the lunch from the input
    for _ in range(s):
        parts = list(map(int, input().split()))
        swan = parts[0]
        for lunch in parts[1:]:
            del caps[swan][s + lunch] # delete the edge from swan to that lunch

    print(ford_fulkerson(caps, src, sink))

main()
