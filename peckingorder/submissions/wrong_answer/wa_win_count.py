#wa_win_count.py
#initial thoughts: this is miras first attempt from the story
#just rank swans by how many displacements they won (out-degree), most wins first
#false assumption: more wins = higher rank. wins only count log entries, not who they
#were against, eg 3 -> 1 -> 4 -> 2 gives 3, 1 and 4 one win each so the order between
#them is just a tie-break. also never reports AMBIGUOUS or CONTRADICTORY
#expected verdict: WRONG ANSWER (already fails sample 1)
import sys

#read input, only need the winner of each entry
def count_wins():
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    wins = [0] * (n + 1)
    for i in range(m):
        a = int(data[2 + 2 * i])
        wins[a] += 1
    return n, wins

n, wins = count_wins()
#sort by wins descending (python sort is stable, so ties stay in number order)
order = sorted(range(1, n + 1), key=lambda v: -wins[v])
print(" ".join(map(str, order)))
