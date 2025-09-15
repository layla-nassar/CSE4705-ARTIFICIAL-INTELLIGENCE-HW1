# grid_search_ldfs_iddfs.py
import time
from typing import Tuple, Dict, List, Optional, Set

from grid import START, GOAL, neighbors, reconstruct_path, SearchResult, write_summary_line

def depth_limited_dfs(limit: int):
    came_from: Dict[Tuple[int,int], Tuple[int,int]] = {START: START}
    visited: Set[Tuple[int,int]] = set()
    explored = 0
    found_goal = False

    def rec(node, depth) -> Optional[Tuple[Dict, int]]:
        nonlocal explored, found_goal
        explored += 1
        if node == GOAL:
            found_goal = True
            return came_from, explored
        if depth == limit:
            return None
        for nb in neighbors(node):
            if nb not in came_from:  # use came_from as implicit visited for path tree
                came_from[nb] = node
                r = rec(nb, depth+1)
                if r is not None:
                    return r
        return None

    rec(START, 0)
    if found_goal:
        path = reconstruct_path(came_from, START, GOAL)
        return path, explored, False  # optimal not guaranteed
    return [], explored, False

def iddfs(max_limit: int = 200):
    total_explored = 0
    for L in range(max_limit+1):
        came_from: Dict[Tuple[int,int], Tuple[int,int]] = {START: START}
        explored = 0
        found_goal = False
        def rec(node, depth):
            nonlocal explored, found_goal
            explored += 1
            if node == GOAL:
                found_goal = True
                return True
            if depth == L:
                return False
            for nb in neighbors(node):
                if nb not in came_from:
                    came_from[nb] = node
                    if rec(nb, depth+1):
                        return True
            return False
        if rec(START, 0):
            path = reconstruct_path(came_from, START, GOAL)
            total_explored += explored
            return path, total_explored, True  # IDDFS finds shallowest solution => optimal in uniform cost
        total_explored += explored
    return [], total_explored, False

def run_dlds_and_iddfs():
    # DLDFS
    limit = 25  # a reasonable default; you can adjust
    t0 = time.perf_counter()
    dlds_path, dlds_explored, _ = depth_limited_dfs(limit)
    t1 = time.perf_counter()
    dlds_res = SearchResult(
        found = len(dlds_path) > 0,
        path = dlds_path,
        path_length = max(0, len(dlds_path)-1),
        nodes_explored = dlds_explored,
        optimal = False if len(dlds_path)>0 else None,
        exec_time_sec = t1 - t0,
        algorithm = f"DLDFS(L={limit})"
    )

    # IDDFS
    t2 = time.perf_counter()
    iddfs_path, iddfs_explored, _ = iddfs(max_limit=200)
    t3 = time.perf_counter()
    iddfs_res = SearchResult(
        found = len(iddfs_path) > 0,
        path = iddfs_path,
        path_length = max(0, len(iddfs_path)-1),
        nodes_explored = iddfs_explored,
        optimal = True if len(iddfs_path)>0 else None,
        exec_time_sec = t3 - t2,
        algorithm = "IDDFS"
    )
    return dlds_res, iddfs_res

def main():
    from grid import print_grid_with_path
    dlds_res, iddfs_res = run_dlds_and_iddfs()
    for res in [dlds_res, iddfs_res]:
        print(write_summary_line(res))
        if res.found:
            print(f"\n{res.algorithm} path (S=start, G=goal, *=path):")
            print(print_grid_with_path(res.path))
            print()

if __name__ == "__main__":
    main()
