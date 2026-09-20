# TRAP 7: in-degree counted as DISTINCT predecessors, but decremented once
# per edge in the adjacency list (which still holds duplicates).
import sys
from collections import deque
def main():
    d=sys.stdin.buffer.read().split(); n=int(d[0]); m=int(d[1])
    adj=[[] for _ in range(n+1)]; preds=[set() for _ in range(n+1)]; p=2
    for _ in range(m):
        a=int(d[p]); b=int(d[p+1]); p+=2; adj[a].append(b); preds[b].add(a)
    indeg=[len(preds[v]) for v in range(n+1)]
    q=deque(v for v in range(1,n+1) if indeg[v]==0); order=[]; uniq=True
    while q:
        if len(q)>1: uniq=False
        u=q.popleft(); order.append(u)
        for v in adj[u]:
            indeg[v]-=1
            if indeg[v]==0: q.append(v)
    if len(order)<n: print("CONTRADICTORY")
    elif not uniq: print("AMBIGUOUS")
    else: print(" ".join(map(str,order)))
main()
