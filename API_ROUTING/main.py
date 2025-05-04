import sys
from pathfinding import imageToMatrix
from DStarLite import DStarLite


def main():
    grid_map = imageToMatrix("TerminalAv2.png")

    start = tuple(map(int, sys.argv[1].split(',')))
    goal = tuple(map(int, sys.argv[2].split(',')))

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
        temps_per_pixel = 0.4
        temps_total = temps_per_pixel * len(path)
        temps_total = round(temps_total,2)
        print(f"Temps total estimat: {temps_total} segons") 
        #planner.plotPath(path)
    else:
        print("Ruta no trobada.")

if __name__ == "__main__":
    main()
