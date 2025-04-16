from pathfinding import imageToMatrix
from DStarLite import DStarLite

def main():
    grid_map = imageToMatrix("TerminalAv2.png")

    start = (11, 14)
    goal = (26, 56)

    x, y = goal

    if grid_map.isFree(x, y):
        planner = DStarLite(grid_map, start, goal)
        path = planner.getPath()
    else:
        print("Ruta no possible.")

    if path:
        print(f"Ruta trobada amb {len(path)} passos.")
        planner.savePathToJSON(path, 'path.json')
        planner.plotPath(path)
    else:
        print("Ruta no trobada.")

if __name__ == "__main__":
    main()
