import heapq
import math
import json
import matplotlib.pyplot as plt
from collections import defaultdict

class DStarLite:
    def __init__(self, gridMap, start, goal):
        self.map = gridMap
        self.start = start
        self.goal = goal
        self.km = 0

        self.rhs = defaultdict(lambda: math.inf)
        self.g = defaultdict(lambda: math.inf)
        self.rhs[goal] = 0

        self.U = []
        heapq.heappush(self.U, (self.calculateKey(goal), goal))

        self.last = start

    def calculateKey(self, s):
        min_g_rhs = min(self.g[s], self.rhs[s])
        return (min_g_rhs + self.heuristic(self.start, s) + self.km, min_g_rhs)

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def getSuccessors(self, u):
        x, y = u
        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        return [(nx, ny) for nx, ny in neighbors if 0 <= nx < self.map.height and 0 <= ny < self.map.width and self.map.isFree(nx, ny)]

    def updateVertex(self, u):
        if u != self.goal:
            self.rhs[u] = min(
                [self.g[s] + 1 for s in self.getSuccessors(u)] or [math.inf]
            )
        if any(item[1] == u for item in self.U):
            self.U = [item for item in self.U if item[1] != u]
            heapq.heapify(self.U)
        if self.g[u] != self.rhs[u]:
            heapq.heappush(self.U, (self.calculateKey(u), u))

    def computeShortestPath(self):
        while self.U:
            k_old, u = heapq.heappop(self.U)
            k_new = self.calculateKey(u)
            if k_old < k_new:
                heapq.heappush(self.U, (k_new, u))
            elif self.g[u] > self.rhs[u]:
                self.g[u] = self.rhs[u]
                for s in self.getSuccessors(u):
                    self.updateVertex(s)
            else:
                g_old = self.g[u]
                self.g[u] = math.inf
                for s in self.getSuccessors(u) + [u]:
                    self.updateVertex(s)

    def updateObstacle(self, position):
        self.map.grid[position[0]][position[1]] = 1
        for u in self.getSuccessors(position) + [position]:
            self.updateVertex(u)
        self.km += self.heuristic(self.last, self.start)
        self.last = self.start
        self.computeShortestPath()

    def getPath(self):
        self.computeShortestPath()
        path = [self.start]
        current = self.start
        while current != self.goal:
            successors = self.getSuccessors(current)
            if not successors:
                return None
            current = min(successors, key=lambda s: self.g[s] + 1)
            path.append(current)
        return path

    def savePathToJSON(self, path, filename):
        with open(filename, 'w') as f:
            json.dump(path, f)

    def plotPath(self, path):
        grid = self.map.grid.copy()
        for x, y in path:
            grid[x][y] = 2
        plt.scatter([self.start[1]], [self.start[0]], c='green', label='Inici', s=20)
        plt.scatter([self.goal[1]], [self.goal[0]], c='red', label='Final', s=20)
        plt.imshow(grid, cmap='gray_r')
        plt.title('Ruta Òptima')
        plt.legend()
        plt.axis('off')
        #plt.savefig('PathAtoB.png')
        plt.show()
