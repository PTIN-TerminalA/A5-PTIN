from PIL import Image, ImageDraw
import numpy as np

class GridMap:
    def __init__(self, grid: np.ndarray, scale: int):
        self.grid = grid
        self.scale = scale  # Quantitat de píxels per casella
        self.height, self.width = grid.shape

    def isFree(self, x: int, y: int) -> bool:
        #return self.grid[x][y] == 0
        radius = (11 - 1) // 2

        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.height and 0 <= ny < self.width:
                    if self.grid[nx][ny] == 1:
                        return False
                else:
                    return False
        return True

    def printASCII(self):
        '''
        characters = {0: '.', 1: '#'}
        for row in self.grid:
            print(''.join(characters[value] for value in row))
        '''
        for row in self.grid:
            print(' '.join(str(value) for value in row))
            
def imageToMatrix(image_path: str) -> GridMap:
    img = Image.open(image_path).convert('L')

    mtx = np.array(img)
    threshold = 254
    binaryMTX = (mtx < threshold).astype(np.uint8)

    return GridMap(binaryMTX, 1)
   
if __name__ == '__main__':
    gridMap = imageToMatrix('MapTerminalA.jpg')
    #print(f"Value position: {gridMap.grid[144][193]}")
    gridMap.printASCII()

    #start = (144, 193)
    #goal = (416, 120)

    #gridMap.drawPoint(*start, color=(0, 255, 0))  # Green start point
    #gridMap.drawPoint(*goal, color=(0, 0, 255))   # Blue goal point
    