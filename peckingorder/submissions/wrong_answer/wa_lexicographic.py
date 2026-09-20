# TRAP 8: lexicographically smallest topological order via a min-heap.
# Always produces AN order, so it never reports AMBIGUOUS.
import sys, heapq
def main():
    d=sys.stdin.buffer.read().split(); n=int(d[0]); m=int(d[1])
    adj=[[] for _ in range(n+1)]; indeg=[0]*(n+1); p=2
    for _ in range(m):
        a=int(d[p]); b=int(d[p+1]); p+=2; adj[a].append(b); indeg[b]+=1
    h=[v for v in range(1,n+1) if indeg[v]==0]; heapq.heapify(h); order=[]
    while h:
        u=heapq.heappop(h); order.append(u)
        for v in adj[u]:
            indeg[v]-=1
            if indeg[v]==0: heapq.heappush(h,v)
    print("CONTRADICTORY" if len(order)<n else " ".join(map(str,order)))
main()
