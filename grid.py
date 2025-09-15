# grid.py
# CSE 4705 - HW1:

from collections import deque
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional

# 10x10 grid (0=open, 1=wall)
GRID: List[List[int]] = [
    [0,0,0,1,0,0,0,0,0,0],
    [0,1,0,1,0,1,1,1,0,1],
    [0,1,0,0,0,0,0,1,0,0],
    [0,1,1,1,1,1,0,1,1,0],
    [0,0,0,0,0,1,1,0,0,0],
    [1,1,1,1,0,1,1,1,1,0],
    [0,0,0,1,0,0,0,1,0,0],
    [0,1,0,1,1,1,0,1,1,0],
    [0,1,0,0,0,0,0,0,1,0],
    [0,1,1,1,1,1,1,0,0,0],
]

START: Tuple[int, int] = (0, 0)
GOAL:  Tuple[int, int] = (9, 9)

DIRS: List[Tuple[int,int]] = [(1,0),(-1,0),(0,1),(0,-1)]  # 4-neighborhood

def in_bounds(r: int, c: int) -> bool:
    return 0 <= r < len(GRID) and 0 <= c < len(GRID[0])

def passable(r: int, c: int) -> bool:
    return GRID[r][c] == 0

def neighbors(node: Tuple[int,int]) -> List[Tuple[int,int]]:
    r, c = node
    nbrs = []
    for dr, dc in DIRS:
        rr, cc = r+dr, c+dc
        if in_bounds(rr,cc) and passable(rr,cc):
            nbrs.append((rr,cc))
    return nbrs

@dataclass
class SearchResult:
    found: bool
    path: List[Tuple[int,int]]
    path_length: int
    nodes_explored: int
    optimal: Optional[bool]
    exec_time_sec: float
    algorithm: str
    extra: Optional[dict] = None

def reconstruct_path(came_from: Dict[Tuple[int,int], Tuple[int,int]], start, goal) -> List[Tuple[int,int]]:
    if goal not in came_from and goal != start:
        return []
    node = goal
    path = [node]
    while node != start:
        node = came_from[node]
        path.append(node)
    path.reverse()
    return path

def print_grid_with_path(path: List[Tuple[int,int]]) -> str:
    marks = {p: True for p in path}
    lines = []
    for r, row in enumerate(GRID):
        cells = []
        for c, val in enumerate(row):
            if (r,c) == START:
                cells.append('S')
            elif (r,c) == GOAL:
                cells.append('G')
            elif (r,c) in marks:
                cells.append('*')
            else:
                cells.append('.' if val==0 else '#')
        lines.append(' '.join(cells))
    return '\n'.join(lines)

def write_summary_line(res: SearchResult) -> str:
    opt = "Y" if res.optimal else ("N" if res.optimal is not None else "?")
    return f"{res.algorithm},found={res.found},path_len={res.path_length},nodes={res.nodes_explored},optimal={opt},time_sec={res.exec_time_sec:.6f}"
