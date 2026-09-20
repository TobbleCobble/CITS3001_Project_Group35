# TRAP 5: recursive DFS reverse-postorder. Blows the stack on a deep chain.
import sys
def main():
    d=sys.stdin.buffer.read().split(); n=int(d[0]); m=int(d[1])
    adj=[[] for _ in range(n+1)]; p=2
    for _ in range(m):
        a=int(d[p]); b=int(d[p+1]); p+=2; adj[a].append(b)
    state=[0]*(n+1); post=[]
    def dfs(u):
        state[u]=1
        for v in adj[u]:
            if state[v]==1: raise ValueError("cycle")
            if state[v]==0: dfs(v)
        state[u]=2; post.append(u)
    try:
        for s in range(1,n+1):
            if state[s]==0: dfs(s)
    except ValueError:
        print("CONTRADICTORY"); return
    order=post[::-1]
    es={(int(d[2+2*i]),int(d[3+2*i])) for i in range(m)}
    print(" ".join(map(str,order)) if all((order[i],order[i+1]) in es for i in range(n-1)) else "AMBIGUOUS")
main()
