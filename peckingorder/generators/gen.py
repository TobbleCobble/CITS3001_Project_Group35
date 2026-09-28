#gen.py
#test data generator for pecking order
#run from the problem folder:  python3 generators/gen.py
#writes every secret test to data/secret/NN_name.in and works out the matching .ans
#with the same kahns algorithm as submissions/accepted/solution.py
#everything is seeded so running it again gives byte-identical files
#
#what each group of tests is aimed at:
#  small hand-made cases (01-09): every edge case and one tiny counterexample per trap
#  big cases at N = M = 2*10^5 (10-20): time limit, recursion depth, duplicates, and
#  ambiguity / cycles hidden right at the end of a long run
import os
import random
import sys
from collections import deque

MAX_N = 200000
MAX_M = 200000
SEED = 3001

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "secret")


#reference answer (kahns + uniqueness check), same logic as the accepted solution
def solve(n, edges):
    adj = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for a, b in edges:
        adj[a].append(b)
        indeg[b] += 1
    ready = deque(v for v in range(1, n + 1) if indeg[v] == 0)
    order = []
    unique = True
    while ready:
        if len(ready) > 1:
            unique = False
        u = ready.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                ready.append(v)
    if len(order) < n:
        return "CONTRADICTORY"
    if not unique:
        return "AMBIGUOUS"
    return " ".join(map(str, order))


#write one test case and its answer
def emit(name, n, edges, expect=None):
    assert 1 <= n <= MAX_N and 0 <= len(edges) <= MAX_M
    for a, b in edges:
        assert 1 <= a <= n and 1 <= b <= n and a != b
    ans = solve(n, edges)
    #sanity check the generator did what the test name says
    if expect is not None:
        kind = ans if ans in ("AMBIGUOUS", "CONTRADICTORY") else "UNIQUE"
        assert kind == expect, f"{name}: expected {expect}, got {kind}"
    with open(os.path.join(OUT_DIR, name + ".in"), "w") as f:
        f.write(f"{n} {len(edges)}\n")
        f.write("".join(f"{a} {b}\n" for a, b in edges))
    with open(os.path.join(OUT_DIR, name + ".ans"), "w") as f:
        f.write(ans + "\n")
    print(f"{name:32s} n={n:<7d} m={len(edges):<7d} -> {ans[:40]}")


#random relabelling so the answer isnt just 1 2 3 ... n
def random_labels(rnd, n):
    lbl = list(range(1, n + 1))
    rnd.shuffle(lbl)
    return lbl


#a forced ranking: one hamiltonian chain, plus `extra` redundant forward entries
def chain_edges(rnd, lbl, extra=0):
    n = len(lbl)
    edges = [(lbl[i], lbl[i + 1]) for i in range(n - 1)]
    for _ in range(extra):
        i = rnd.randrange(n - 1)
        j = rnd.randrange(i + 1, n)
        edges.append((lbl[i], lbl[j]))
    return edges


#random dag: every entry points forwards in a hidden random order
def random_dag_edges(rnd, lbl, m):
    n = len(lbl)
    edges = []
    for _ in range(m):
        i = rnd.randrange(n - 1)
        j = rnd.randrange(i + 1, n)
        edges.append((lbl[i], lbl[j]))
    return edges


def main():
    rnd = random.Random(SEED)
    os.makedirs(OUT_DIR, exist_ok=True)

    #---- small hand-made cases ----
    #smallest possible input, answer is just "1"
    emit("01_single_swan", 1, [], "UNIQUE")
    #two swans, empty log -> either order works
    emit("02_two_swans_no_log", 2, [], "AMBIGUOUS")
    #two swans, one entry each way -> 2-cycle
    emit("03_two_swans_both_ways", 2, [(1, 2), (2, 1)], "CONTRADICTORY")
    #unique chain 4 1 5 3 6 2 with redundant shortcut entries
    emit("04_small_redundant_unique", 6,
         [(4, 1), (1, 5), (5, 3), (3, 6), (6, 2), (4, 5), (1, 3), (5, 2)], "UNIQUE")
    #diamond closed off by 3 -> 4, so still one ranking
    emit("05_small_diamond_unique", 4, [(1, 2), (2, 3), (2, 4), (3, 4)], "UNIQUE")
    #1 -> 3 logged twice: counting distinct bosses but removing every copy
    #puts 3 in the ready pool next to 2 (kills wa_distinct_indegree)
    emit("06_small_duplicate_entry", 3, [(1, 3), (1, 3), (2, 3), (1, 2)], "UNIQUE")
    #two top swans (a choice) AND a cycle 3 -> 4 -> 5 -> 3 (kills wa_early_exit)
    emit("07_small_choice_then_cycle", 5,
         [(1, 3), (2, 3), (3, 4), (4, 5), (5, 3)], "CONTRADICTORY")
    #cycle with no choice point before it, the ready pool never has 2 swans
    emit("08_small_hidden_cycle", 4, [(1, 2), (2, 3), (3, 4), (4, 2)], "CONTRADICTORY")
    #forced until the very last step, then 3 and 4 are tied
    emit("09_small_last_step_ambiguous", 4, [(1, 2), (2, 3), (2, 4)], "AMBIGUOUS")

    #---- large cases ----
    #one chain through all 2*10^5 swans: deep recursion + quadratic reachability both die
    lbl = random_labels(rnd, MAX_N)
    edges = chain_edges(rnd, lbl)
    rnd.shuffle(edges)
    emit("10_chain_max", MAX_N, edges, "UNIQUE")

    #forced ranking of 10^5 swans with 10^5 extra redundant entries, many repeated
    lbl = random_labels(rnd, 100000)
    edges = chain_edges(rnd, lbl, extra=MAX_M - 99999 - 30000)
    edges += [edges[rnd.randrange(len(edges))] for _ in range(30000)]   #duplicates
    rnd.shuffle(edges)
    emit("11_chain_redundant_dupes", 100000, edges, "UNIQUE")

    #random dag at N = M = 2*10^5, lots of choice points
    lbl = random_labels(rnd, MAX_N)
    edges = random_dag_edges(rnd, lbl, MAX_M)
    emit("12_random_dag_max", MAX_N, edges, "AMBIGUOUS")

    #random graph at N = M = 2*10^5 with entries in any direction, plus a planted
    #long cycle so there is definitely one (and plenty of choice points before it)
    edges = []
    for _ in range(MAX_M - 1000):
        a = rnd.randint(1, MAX_N)
        b = rnd.randint(1, MAX_N - 1)
        if b >= a:
            b += 1
        edges.append((a, b))
    cyc = rnd.sample(range(1, MAX_N + 1), 1000)
    edges += [(cyc[i], cyc[(i + 1) % 1000]) for i in range(1000)]
    rnd.shuffle(edges)
    emit("13_random_cyclic_max", MAX_N, edges, "CONTRADICTORY")

    #forced for 2*10^5 - 2 steps, then the last two swans are tied
    lbl = random_labels(rnd, MAX_N)
    edges = [(lbl[i], lbl[i + 1]) for i in range(MAX_N - 2)]   #chain to lbl[-2]
    edges.append((lbl[-3], lbl[-1]))                            #lbl[-1] also below lbl[-3]
    edges.append((lbl[0], lbl[-1]))                             #pad m up to exactly 2*10^5
    rnd.shuffle(edges)
    emit("14_last_step_ambiguous_max", MAX_N, edges, "AMBIGUOUS")

    #a full chain with the last entry flipped back into a 2-cycle: never a choice,
    #the contradiction only shows up at the end
    lbl = random_labels(rnd, MAX_N)
    edges = chain_edges(rnd, lbl)
    edges.append((lbl[-1], lbl[-2]))
    rnd.shuffle(edges)
    emit("15_chain_late_cycle_max", MAX_N, edges, "CONTRADICTORY")

    #N = 2 with every one of the 2*10^5 entries the same displacement
    emit("16_two_swans_all_duplicates", 2, [(2, 1)] * MAX_M, "UNIQUE")

    #N = 2, 10^5 copies each way
    edges = [(1, 2)] * (MAX_M // 2) + [(2, 1)] * (MAX_M // 2)
    rnd.shuffle(edges)
    emit("17_two_swans_duplicates_both_ways", 2, edges, "CONTRADICTORY")

    #1200 swans, dense log: chain plus ~2*10^5 redundant/duplicate entries
    lbl = random_labels(rnd, 1200)
    edges = chain_edges(rnd, lbl, extra=MAX_M - 1199)
    rnd.shuffle(edges)
    emit("18_dense_unique", 1200, edges, "UNIQUE")

    #one boss above 2*10^5 - 1 swans, nothing else known
    lbl = random_labels(rnd, MAX_N)
    edges = [(lbl[0], lbl[i]) for i in range(1, MAX_N)]
    rnd.shuffle(edges)
    emit("19_star_ambiguous_max", MAX_N, edges, "AMBIGUOUS")

    #full chain with a single link missing in the middle
    lbl = random_labels(rnd, MAX_N)
    edges = chain_edges(rnd, lbl)
    del edges[MAX_N // 2]
    rnd.shuffle(edges)
    emit("20_chain_one_gap_max", MAX_N, edges, "AMBIGUOUS")


if __name__ == "__main__":
    main()
