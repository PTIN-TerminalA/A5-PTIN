from PIL import Image, ImageDraw
import numpy as np

class GridMap:
    def __init__(self, grid: np.ndarray, scale: int, footprint: int):
        self.grid = grid
        self.scale = scale  # Quantitat de píxels per casella
        self.height, self.width = grid.shape
        self.footprint = footprint

        self.sat = np.zeros((self.height + 1, self.width + 1), dtype=np.int32)
        self.sat[1:, 1:] = np.cumsum(np.cumsum(self.grid, axis=0), axis=1)

    def isFree(self, x: int, y: int) -> bool:
        #return self.grid[x][y] == 0

        f = self.footprint
        if x < 0 or y < 0 or x + f > self.height or y + f > self.width:
            return False

        sum == 0
        return self.areaSum(x, y, x + f, y + f) == 0

    def printASCII(self):
        for row in self.grid:
            print(' '.join(str(value) for value in row))

    def areaSum(self, x0: int, y0: int, x1: int, y1: int) -> int:
        return (
            self.sat[x1, y1]
            - self.sat[x0, y1]
            - self.sat[x1, y0]
            + self.sat[x0, y0]
        )

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

    return GridMap(binaryMTX, 1, 15)

    