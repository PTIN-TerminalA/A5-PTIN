from PIL import Image
import numpy as np

class GridMap:
    def __init__(self, grid: np.ndarray, scale: int):
        self.grid = grid
        self.scale = scale  # Quantitat de píxels per casella
        self.height, self.width = grid.shape

    def isFree(self, x: int, y: int) -> bool:
        return self.grid[x][y] == 0

    def printGrid(self):
        for row in self.grid:
            for value in row:
                print(value, end='')
            print()

    def printASCII(self):
        characters = {0: '.', 1: '#'}
        for row in self.grid:
            print(''.join(characters[value] for value in row))

def imageToMatrixResize(image_path: str, mida=(636, 429)) -> GridMap:
    img = Image.open(image_path).convert('L')
    img = img.resize(mida, Image.Resampling.LANCZOS)

    mtx = np.array(img)
    threshold = 254
    binaryMTX = (mtx < threshold).astype(np.uint8)

    scaleX = 2542 // mida[0]
    scaleY = 1715 // mida[1]

    scale = min(scaleX, scaleY)

    return GridMap(binaryMTX, scale)

def imageToMatrix(image_path: str) -> GridMap:
    img = Image.open(image_path).convert('L')

    mtx = np.array(img)
    threshold = 254
    binaryMTX = (mtx < threshold).astype(np.uint8)

    return GridMap(binaryMTX, 1)
    
#if __name__ == '__main__':
    #gridMap = imageToMatrixResize('NeoTerminalA.png')
    #gridMap = imageToMatrix('TerminalAv3.png')
    #gridMap.printASCII()
    #gridMap.printGrid()