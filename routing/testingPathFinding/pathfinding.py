import heapq, json
from collections import deque
from typing import List, Tuple, Optional, Dict

class PathFinding:
    def __init__(self, gridMap):
        self.map = gridMap

    def getNeighbors(self, node: Tuple[int, int]) -> List[Tuple[int, int]]:
        x, y = node
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.map.height and 0 <= ny < self.map.width and self.map.isFree(nx, ny):
                neighbors.append((nx, ny))
        return neighbors

    def reconstructPath(self, predecessors: Dict[Tuple[int, int], Tuple[int, int]], current: Tuple[int, int]) -> List[Tuple[int, int]]:
        path = [current]
        while current in predecessors:
            current = predecessors[current]
            path.append(current)
        path.reverse()
        return path

    def savePathToJSON(self, path: List[Tuple[int, int]], filename: str) -> None:
        maxX = max(self.map.height - 1, 1)
        maxY = max(self.map.width - 1, 1)

        normalizedPath = [
            ((y / maxY), 1 - (x / maxX)) for (x, y) in path
        ]
        with open(filename, 'w') as f:
            json.dump(normalizedPath, f, indent=1)

class AStar(PathFinding):
    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def findPath(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        if start == goal:
            return [start]

        queue = []
        heapq.heappush(queue, (self.heuristic(start, goal), 0, start))

        predecessors: Dict[Tuple[int, int], Tuple[int, int]] = {}
        cost: Dict[Tuple[int, int], int] = {start: 0}

        while queue:
            _, currentCost, current = heapq.heappop(queue)

            if current == goal:
                return self.reconstructPath(predecessors, current)

            for neighbor in self.getNeighbors(current):
                nouCost = currentCost + 1
                if neighbor in cost and nouCost >= cost[neighbor]:
                    continue
                predecessors[neighbor] = current
                cost[neighbor] = nouCost
                heuristicValue = nouCost + self.heuristic(neighbor, goal)
                heapq.heappush(queue, (heuristicValue, nouCost, neighbor))

        return None

class MultiTargetPathFinding(PathFinding):
    def findPath(self, start: Tuple[int, int], targets: List[Tuple[int, int]]) -> Optional[Tuple[Tuple[int, int], List[Tuple[int, int]]]]:
        if start in targets:
            return (start, [start])

        targetSet = set(targets)
        visited = [[False for _ in range(self.map.width)] for _ in range(self.map.height)]
        queue = deque([start])
        predecessors: Dict[Tuple[int, int], Tuple[int, int]] = {}
        visited[start[0]][start[1]] = True

        while queue:
            current = queue.popleft()
            if current in targetSet:
                path = self.reconstructPath(predecessors, current)
                return (current, path)
            for neighbor in self.getNeighbors(current):
                x, y = neighbor
                if not visited[x][y]:
                    visited[x][y] = True
                    predecessors[neighbor] = current
                    queue.append(neighbor)
        return None