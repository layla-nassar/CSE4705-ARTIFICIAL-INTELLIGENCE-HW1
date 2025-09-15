# run_all.py
# Convenience runner that executes all algorithms and writes a CSV summary.
import csv
from grid_search_bfs_dfs_ucs import bfs, dfs, ucs
from grid_search_ldfs_iddfs import run_dlds_and_iddfs
from grid_search_astar import astar

def main():
    results = [bfs(), dfs(), ucs()]
    dl, idd = run_dlds_and_iddfs()
    results.extend([dl, idd, astar()])

    # Write CSV
    with open("summary.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["algorithm", "found", "path_length", "nodes_explored", "optimal", "exec_time_sec"])
        for r in results:
            w.writerow([r.algorithm, r.found, r.path_length, r.nodes_explored, r.optimal, f"{r.exec_time_sec:.6f}"])
    print("Wrote summary.csv")
    for r in results:
        print(f"{r.algorithm:18} | found={r.found} | path={r.path_length} | nodes={r.nodes_explored} | optimal={r.optimal} | time={r.exec_time_sec:.6f}s")

if __name__ == "__main__":
    main()
