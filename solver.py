from collections import deque

def find_shortest_path(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    visited = set()
    queue = deque([(start, [start])])

    while queue:
        (y, x), path = queue.popleft()
        if (y, x) == end:
            return path

        for dy, dx in [(0,1), (1,0), (0,-1), (-1,0)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < rows and 0 <= nx < cols and maze[ny][nx] == 0 and (ny, nx) not in visited:
                visited.add((ny, nx))
                queue.append(((ny, nx), path + [(ny, nx)]))

    return []
