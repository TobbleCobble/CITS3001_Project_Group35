# TRAP 1: rank by number of displacements won (out-degree), descending.
import sys
def main():
    d=sys.stdin.buffer.read().split(); n=int(d[0]); m=int(d[1])
    wins=[0]*(n+1); p=2
    for _ in range(m):
        a=int(d[p]); p+=2; wins[a]+=1
    order=sorted(range(1,n+1), key=lambda v:-wins[v])
    print(" ".join(map(str,order)))
main()
