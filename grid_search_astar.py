# grid_search_astar.py
import time, heapq
from typing import Tuple, Dict, List

from grid import GRID, START, GOAL, neighbors, reconstruct_path, SearchResult, write_summary_line

def manhattan(a: Tuple[int,int], b: Tuple[int,int]) -> int:
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar():
    t0 = time.perf_counter()
    pq: List[Tuple[int, Tuple[int,int]]] = []
    heapq.heappush(pq, (0, START))
    came_from: Dict[Tuple[int,int], Tuple[int,int]] = {START: START}
    g: Dict[Tuple[int,int], int] = {START: 0}
    explored = 0

    while pq:
        _, cur = heapq.heappop(pq)
        explored += 1
        if cur == GOAL:
            break
        for nb in neighbors(cur):
            tentative = g[cur] + 1
            if nb not in g or tentative < g[nb]:
                g[nb] = tentative
                came_from[nb] = cur
                f = tentative + manhattan(nb, GOAL)
                heapq.heappush(pq, (f, nb))

    path = reconstruct_path(came_from, START, GOAL)
    t1 = time.perf_counter()
    found = len(path) > 0
    optimal = True if found else None  # with admissible & consistent heuristic (Manhattan), A* is optimal
    return SearchResult(found, path, max(0, len(path)-1), explored, optimal, t1-t0, "A* (Manhattan)")

def main():
    res = astar()
    print(write_summary_line(res))
    if res.found:
        from grid import print_grid_with_path
        print(f"\nA* path (S=start, G=goal, *=path):")
        print(print_grid_with_path(res.path))

if __name__ == "__main__":
    main()
