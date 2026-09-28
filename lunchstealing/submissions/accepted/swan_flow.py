"""
ACCEPTED - maximum bipartite matching solved as maximum flow (Ford-Fulkerson).

Reduction:
  - one side of the graph is the swans, the other side is the lunches;
  - an edge swan -> lunch exists when the swan is NOT scared of that student;
  - add a super-source s with an edge s -> every swan, and a super-sink t
    with an edge every lunch -> t, and give every edge capacity 1.
The capacity-1 edges enforce the rules: each swan is used at most once
(s -> swan) and each lunch is stolen at most once (lunch -> t). A unit of
flow therefore traces s -> swan -> lunch -> t, i.e. one successful steal,
so the maximum flow equals the maximum number of lunches the flock can take.

Ford-Fulkerson repeatedly finds an augmenting path in the residual graph and
pushes flow along it; the back-edges let it reroute an earlier assignment,
which is exactly what a greedy cannot do (see the wrong_answer submissions).
Runs comfortably within the limit for S, L <= 100.
"""
from math import inf


def ford_fulkerson(caps, s, t):
    # make sure every edge has a reverse partner (capacity 0) for the residual graph
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
    # DFS through the residual graph: step u -> v only if v is unvisited and the
    # edge still has spare capacity (flow below capacity). Back-edges qualify too,
    # because a pushed edge leaves its reverse with capacity 0 but flow -f < 0.
    parents = {}
    stack = [(s, s)]
    while stack:
        p, u = stack.pop()
        parents[u] = p
        for v in caps[u]:
            if v not in parents and flows[u][v] < caps[u][v]:
                stack.append((u, v))
    if t not in parents:
        return None
    path = [t]
    while path[-1] != s:
        path.append(parents[path[-1]])
    path.reverse()
    return path


def push_flow(caps, flows, path):
    # bottleneck = smallest remaining capacity along the path
    bottleneck = inf
    for u, v in zip(path, path[1:]):
        bottleneck = min(bottleneck, caps[u][v] - flows[u][v])
    # add flow forward, subtract on the reverse edge (opens the reroute option)
    for u, v in zip(path, path[1:]):
        flows[u][v] += bottleneck
        flows[v][u] -= bottleneck
    return bottleneck


def main():
    S, L = map(int, input().split())
    N = S + L + 2
    SRC, SINK = 0, N - 1               # node 0 = source, node N-1 = sink
    # swans occupy indices 1..S, lunches occupy indices S+1..S+L
    caps = {u: {} for u in range(N)}
    for swan in range(1, S + 1):
        caps[SRC][swan] = 1            # source -> swan
    for swan in range(1, S + 1):
        for lunch in range(1, L + 1):
            caps[swan][S + lunch] = 1  # swan -> every lunch (allowed by default)
    for lunch in range(1, L + 1):
        caps[S + lunch][SINK] = 1      # lunch -> sink

    for _ in range(S):
        parts = list(map(int, input().split()))
        swan = parts[0]
        for lunch in parts[1:]:        # students this swan fears
            del caps[swan][S + lunch]  # too scared -> remove that edge

    print(ford_fulkerson(caps, SRC, SINK))


main()
