from maze_generator import generate_maze
from solver import find_shortest_path

class GameState:
    def __init__(self, base_width=11, base_height=11):
        self.level = 1
        self.base_width = base_width
        self.base_height = base_height
        self._generate_new_maze()

    def _generate_new_maze(self):
        self.width = self.base_width + (self.level - 1) * 2
        self.height = self.base_height + (self.level - 1) * 2
        self.maze = generate_maze(self.width, self.height)
        self.start = (1, 1)
        self.end = (self.height - 2, self.width - 2)
        self.solution = find_shortest_path(self.maze, self.start, self.end)
        self.user_path = []

    def submit(self):
        return self.user_path == self.solution

    def next_level(self):
        self.level += 1
        self._generate_new_maze()
