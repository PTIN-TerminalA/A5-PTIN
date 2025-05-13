from datastructure import imageToMatrix, GridMap
from PIL import Image, ImageDraw
from pathfinding import AStar, MultiTargetPathFinding 
import numpy as np
import matplotlib.pyplot as plt
#from astarCython import PathFinding

def main():
    manual_grid = np.array([
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
        [0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0],
        [0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0],
        [0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,0,1,0,1,0],
        [0,1,0,1,0,1,0,0,0,0,0,0,0,0,1,0,1,0,1,0],
        [0,1,0,1,0,1,0,1,1,1,1,1,1,0,1,0,1,0,1,0],
        [0,1,0,1,0,1,0,1,0,0,0,0,1,0,1,0,1,0,1,0],
        [0,1,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,1,0],
        [0,1,0,1,0,1,0,1,0,1,0,0,1,0,1,0,1,0,1,0],
        [0,1,0,1,0,1,0,1,0,1,1,1,1,0,1,0,1,0,1,0],
        [0,1,0,1,0,1,0,1,0,0,0,0,0,0,1,0,1,0,1,0],
        [0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,0,1,0,1,0],
        [0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,0],
        [0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0],
        [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
        [0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    ], dtype=np.uint8)
    
    #gridMap = GridMap(manual_grid, scale=1)
    #gridMap.printASCII()
    gridMap = imageToMatrix('MapTerminalA.jpg')  # tu archivo de imagen

    start = (339, 347)
    targets = [(347, 90), (342, 680), (338, 1025)]
    #goal = (702, 1335)
    #x, y = goal
    pf = MultiTargetPathFinding(gridMap)
    res = pf.findPath(start, targets)
    #pf = JumpPointSearch(gridMap, start, goal)
    #path = pf.search()
    #pf = AStar(gridMap)
    #pf = PathFinding(gridMap, start, goal)
    #path = pf.findPath(start, goal)
    #path = pf.search()
    if res:
        point, path = res
        pf.savePathToJSON(path, 'path.json')
        print(point)

    '''
    # Visualización
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(manual_grid, cmap='Greys', origin='upper')

    # Dibujar el camino en rojo
    x_coords, y_coords = zip(*path)
    ax.plot(y_coords, x_coords, color='red', linewidth=2, label='Camino')

    # Marcar inicio y fin
    ax.plot(path[0][1], path[0][0], 'go', label='Inicio')
    ax.plot(path[-1][1], path[-1][0], 'bo', label='Fin')

    #ax.plot(10, 10, 'bo', label='Fin')
    ax.set_xticks(np.arange(0, 20))
    ax.set_yticks(np.arange(0, 20))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(True, which='both', color='lightgray', linewidth=0.5)
    #ax.legend()
    plt.title("Camino manual desde (0, 0) hasta (19, 19)")
    plt.savefig('PathAtoB.png')
    
    #plt.show()
    #print("-----")
    #print(pathJ)
    #pf = PathFinding(gridMap)
    #path = pf.find_path(start, goal)

    #pf.savePathToJSON(path, 'path.json')
    #pf.plotPath(path)
    #if grid_map.isFree(x, y):
    #    planner = DStarLite(grid_map, start, goal)
    #    path = planner.getPath()
    #else:
    #    print("Ruta no possible.")

    #if path:
    #    print(f"Ruta trobada amb {len(path)} passos.")
    #    planner.savePathToJSON(path, 'path.json')
    #    planner.plotPath(path)
    #else:
    #    print("Ruta no trobada.")
    '''
    '''
    # Carga desde imagen (o usa manual grid)
    #gridMap = imageToMatrix('MapaTerminalA.png')  # tu archivo de imagen

    #start = (50, 50)
    #goal = (118, 118)

    # Ejecutar búsqueda JPS en Cython
    pf = PathFinding(gridMap, start, goal)
    path = pf.search()

    if not path:
        print("No se encontró ruta")
        return

    # Visualización
    mtx = gridMap.grid
    fig, ax = plt.subplots(figsize=(6,6))
    ax.imshow(mtx, cmap='Greys', origin='upper')

    x_coords, y_coords = zip(*path)
    ax.plot(y_coords, x_coords, linewidth=2, label='Ruta')
    ax.plot(start[1], start[0], 'go', label='Inicio')
    ax.plot(goal[1], goal[0], 'ro', label='Fin')

    ax.set_xticks(np.arange(0, gridMap.width))
    ax.set_yticks(np.arange(0, gridMap.height))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(True, which='both', linewidth=0.5)
    ax.legend()
    plt.title(f"Ruta de {start} a {goal}")
    plt.savefig('PathAtoBCython.png')
    print(f"Ruta guardada en PathAtoB.png con {len(path)} pasos.")
    #gridMap = imageToMatrix('MapaTerminalA.png')

    start = (19, 19)
    goal = (10, 10)

    pf = PathFinding(gridMap, start, goal)
    path = pf.search()

    #print(f"Value position: {gridMap.grid[193][144]}")
    #print(f"Value position: {gridMap.grid[120][416]}")
    '''
    
    if path:
        #print("Path found:", path)
        
        # Optionally, draw the path on the grid image
        img = Image.fromarray(gridMap.grid * 255).convert("RGB")  # Convert grid to image
        draw = ImageDraw.Draw(img)

        # Draw the path as a sequence of points (you can change the color)
        for (x, y) in path:
            draw.point((y, x), fill=(255, 0, 0))  # Red color for the path
        
        img.show()  # Display the image with the path
        
    else:
        print("No path found")
    
if __name__ == "__main__":
    main()
