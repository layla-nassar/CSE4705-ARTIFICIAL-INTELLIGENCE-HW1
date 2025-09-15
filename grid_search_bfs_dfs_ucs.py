# grid_search_bfs_dfs_ucs.py
import time
from collections import deque
import heapq
from typing import Tuple, Dict, List, Set

from grid import GRID, START, GOAL, neighbors, reconstruct_path, SearchResult, write_summary_line

def bfs() -> SearchResult:
    t0 = time.perf_counter()
    frontier = deque([START])
    came_from: Dict[Tuple[int,int], Tuple[int,int]] = {START: START}
    explored = 0
    while frontier:
        cur = frontier.popleft()
        explored += 1
        if cur == GOAL:
            break
        for nb in neighbors(cur):
            if nb not in came_from:
                came_from[nb] = cur
                frontier.append(nb)
    path = reconstruct_path(came_from, START, GOAL)
    t1 = time.perf_counter()
    found = len(path) > 0
    # BFS on uniform step cost graph yields shortest path
    optimal = True if found else None
    return SearchResult(found, path, max(0, len(path)-1), explored, optimal, t1-t0, "BFS")

def dfs() -> SearchResult:
    t0 = time.perf_counter()
    stack: List[Tuple[int,int]] = [START]
    came_from: Dict[Tuple[int,int], Tuple[int,int]] = {START: START}
    visited: Set[Tuple[int,int]] = set([START])
    explored = 0
    while stack:
        cur = stack.pop()
        explored += 1
        if cur == GOAL:
            break
        for nb in neighbors(cur):
            if nb not in visited:
                visited.add(nb)
                came_from[nb] = cur
                stack.append(nb)
    path = reconstruct_path(came_from, START, GOAL)
    t1 = time.perf_counter()
    found = len(path) > 0
    # DFS is not guaranteed optimal
    optimal = False if found else None
    return SearchResult(found, path, max(0, len(path)-1), explored, optimal, t1-t0, "DFS")

def ucs() -> SearchResult:
    t0 = time.perf_counter()
    pq: List[Tuple[int, Tuple[int,int]]] = [(0, START)]  # (cost, node)
    came_from: Dict[Tuple[int,int], Tuple[int,int]] = {START: START}
    cost_so_far: Dict[Tuple[int,int], int] = {START: 0}
    explored = 0
    while pq:
        cost, cur = heapq.heappop(pq)
        explored += 1
        if cur == GOAL:
            break
        for nb in neighbors(cur):
            new_cost = cost_so_far[cur] + 1  # unit step cost
            if nb not in cost_so_far or new_cost < cost_so_far[nb]:
                cost_so_far[nb] = new_cost
                came_from[nb] = cur
                heapq.heappush(pq, (new_cost, nb))
    path = reconstruct_path(came_from, START, GOAL)
    t1 = time.perf_counter()
    found = len(path) > 0
    # With unit step costs, UCS finds an optimal path
    optimal = True if found else None
    return SearchResult(found, path, max(0, len(path)-1), explored, optimal, t1-t0, "UCS")

def main():
    results = [bfs(), dfs(), ucs()]
    for res in results:
        print(write_summary_line(res))
        if res.found:
            print(f"\n{res.algorithm} path (S=start, G=goal, *=path):")
            from grid import print_grid_with_path
            print(print_grid_with_path(res.path))
            print()

if __name__ == "__main__":
    main()
