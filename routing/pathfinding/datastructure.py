from PIL import Image, ImageDraw
import numpy as np

class GridMap:
    def __init__(self, grid: np.ndarray, scale: int):
        self.grid = grid
        self.scale = scale  # Quantitat de píxels per casella
        self.height, self.width = grid.shape

    def isFree(self, x: int, y: int) -> bool:
        return self.grid[x][y] == 0

    def printASCII(self):
        '''
        characters = {0: '.', 1: '#'}
        for row in self.grid:
            print(''.join(characters[value] for value in row))
        '''
        for row in self.grid:
            print(' '.join(str(value) for value in row))

    def drawPoint(self, x: int, y: int, color: tuple = (255, 0, 0), radius: int = 1):
        # Convert grid to an image to draw points
        img = Image.fromarray(self.grid * 255)  # Scaling 0->255 for visualization
        img = img.convert("RGB")  # Convert to RGB mode
        draw = ImageDraw.Draw(img)
        # Draw a colored circle at the coordinates (x, y)
        draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=color)
        img.show()  # Show the image with the point

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
    