"""
Escape the Labyrinth of Ancient France
--------------------------------------

You must implement TWO functions:
1) generate_maze(rows, cols)
2) astar(maze, start, goal)

Everything else (graphics, animation, game loop) is already provided for you below
Do NOT modify the visualization codes
"""

import pygame
import random
import heapq
import math

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 40, 40
CELL = WIDTH // COLS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escape the Labyrinth of Ancient France")

# ============================================================
# ================== PART 1: MAZE GENERATION =================
# ============================================================
def generate_maze(rows: int, cols: int) -> list[list[int]]:
    """
    Generate a PERFECT maze using Randomized Prim's Algorithm.

    Parameters:
        rows (int): Number of rows in the maze grid
        cols (int): Number of columns in the maze grid

    Returns:
        maze (list[list[int]]):
            2D grid where:
                0 = open cell (walkable)
                1 = wall

    Requirements:
        - Start with a grid full of walls (all 1s)
        - Use Randomized Prim's Algorithm (or equivalent MST-based carving)
        - The maze must be PERFECT:
            * Exactly one path between any two open cells
        - Ensure start (0,0) and goal (rows-1, cols-1) are open
    """

    # Step 1: Initialize grid full of walls
    maze = [[1 for _ in range(cols)] for _ in range(rows)]

    # Step 2: Implement Randomized Prim's Algorithm
    # Cells occupy even-indexed positions; walls sit between them at odd indices.
    # Moving from cell (r, c) two steps to (r+2, c) passes through wall (r+1, c).

    def add_walls(r, c):
        for dr, dc in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 1:
                walls.append((r + dr // 2, c + dc // 2, nr, nc))

    maze[0][0] = 0
    walls = []
    add_walls(0, 0)

    while walls:
        idx = random.randrange(len(walls))
        wall_r, wall_c, cell_r, cell_c = walls.pop(idx)
        if maze[cell_r][cell_c] == 1:
            maze[wall_r][wall_c] = 0
            maze[cell_r][cell_c] = 0
            add_walls(cell_r, cell_c)

    # Ensure entrance and exit are open
    maze[0][0] = 0
    maze[rows - 1][cols - 1] = 0

    return maze


# ============================================================
# ================== PART 2: A* SEARCH =======================
# ============================================================

def heuristic(a: tuple, b: tuple) -> float:
    """
    Compute Euclidean distance between two cells.

    Required because diagonal movement is allowed.
    """
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


def astar(maze: list[list[int]], start: tuple, goal: tuple) -> list[tuple]:
    """
    Perform A* Search on the maze.

    Parameters:
        maze (list[list[int]]): 2D grid returned by generate_maze()
        start (tuple): (row, col)
        goal (tuple): (row, col)

    Returns:
        path (list[tuple]):
            Ordered list of coordinates from start to goal (inclusive).
            Return [] if no path exists.

    Movement Rules:
        - 8-directional movement allowed
            (up, down, left, right, and diagonals)
        - Cost = 1 for horizontal/vertical moves
        - Cost = sqrt(2) for diagonal moves
    """

    # Direction vectors (DO NOT MODIFY)
    directions = [
        (1, 0), (-1, 0), (0, 1), (0, -1),
        (1, 1), (1, -1), (-1, 1), (-1, -1)
    ]

    rows, cols = len(maze), len(maze[0])
    g_score = {start: 0.0}
    came_from = {}
    counter = 0
    open_set = [(heuristic(start, goal), counter, start)]
    visited = set()

    while open_set:
        _, _, current = heapq.heappop(open_set)

        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for dr, dc in directions:
            nr, nc = current[0] + dr, current[1] + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0:
                neighbor = (nr, nc)
                move_cost = math.sqrt(2) if dr != 0 and dc != 0 else 1.0
                tentative_g = g_score[current] + move_cost
                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    counter += 1
                    heapq.heappush(open_set, (tentative_g + heuristic(neighbor, goal), counter, neighbor))

    return []


# ============================================================
# ================== VISUALIZATION (DO NOT EDIT) =============
# ============================================================

def draw_maze(maze):
    screen.fill(WHITE)
    for r in range(ROWS):
        for c in range(COLS):
            if maze[r][c] == 1:
                pygame.draw.rect(screen, BLACK, (c*CELL, r*CELL, CELL, CELL))
    pygame.display.update()


# ---------------- MAIN ----------------
def main():
    maze = generate_maze(ROWS, COLS)

    start = (0, 0)
    goal = (ROWS - 1, COLS - 1)

    draw_maze(maze)

    # Draw start and goal
    pygame.draw.rect(screen, GREEN, (start[1]*CELL, start[0]*CELL, CELL, CELL))
    pygame.draw.rect(screen, RED, (goal[1]*CELL, goal[0]*CELL, CELL, CELL))
    pygame.display.update()

    path = astar(maze, start, goal)

    if path:
        for node in path:
            pygame.time.delay(20)
            pygame.draw.rect(screen, BLUE, (node[1]*CELL, node[0]*CELL, CELL, CELL))
            pygame.display.update()

    # Keep window open
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


if __name__ == "__main__":
    main()
