# TRAP 4: return AMBIGUOUS as soon as two sources are available,
# without finishing the run to check for a cycle elsewhere.
import sys
from collections import deque
def main():
    d=sys.stdin.buffer.read().split(); n=int(d[0]); m=int(d[1])
    adj=[[] for _ in range(n+1)]; indeg=[0]*(n+1); p=2
    for _ in range(m):
        a=int(d[p]); b=int(d[p+1]); p+=2; adj[a].append(b); indeg[b]+=1
    q=deque(v for v in range(1,n+1) if indeg[v]==0); order=[]
    while q:
        if len(q)>1:
            print("AMBIGUOUS"); return          # <-- premature
        u=q.popleft(); order.append(u)
        for v in adj[u]:
            indeg[v]-=1
            if indeg[v]==0: q.append(v)
    print("CONTRADICTORY" if len(order)<n else " ".join(map(str,order)))
main()
