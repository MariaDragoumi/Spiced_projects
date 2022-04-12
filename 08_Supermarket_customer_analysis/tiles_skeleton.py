import numpy as np
import cv2
import algoritm_moves



TILE_SIZE = 32

MARKET = """
##################
##..............##
##..##..##..#e..B#
##..##..##..#s..o#
##..##..##..#g..a#
##..##..##..#m..c#
##..##..##..#b..p#
##..............##
##..C#..C#..C#..##
##..##..##..##..##
##..............##
##############GG##
""".strip()


class SupermarketMap:
    """Visualizes the supermarket background"""

    def __init__(self, layout, tiles):
        """
        layout : a string with each character representing a tile
        tiles   : a numpy array containing all the tile images
        """
        self.tiles = tiles
        # split the layout string into a two dimensional matrix
        self.contents = [list(row) for row in layout.split("\n")]
        self.ncols = len(self.contents[0])
        self.nrows = len(self.contents)
        self.image = np.zeros(
            (self.nrows*TILE_SIZE, self.ncols*TILE_SIZE, 3), dtype=np.uint8
        )
        self.prepare_map()

    def extract_tile(self, row, col):
        """extract a tile array from the tiles image"""
        y = row*TILE_SIZE
        x = col*TILE_SIZE
        return self.tiles[y:y+TILE_SIZE, x:x+TILE_SIZE]

    def get_tile(self, char):
        """returns the array for a given tile character"""
        if char == "#":
            return self.extract_tile(0, 0)
        elif char == "G":
            return self.extract_tile(7, 3)
        elif char == "C":
            return self.extract_tile(2, 8)

### adding fruits
        elif char == "b":
            return self.extract_tile(0, 4)
        elif char == "m":
            return self.extract_tile(3, 4)
        elif char == "g":
            return self.extract_tile(4, 4)
        elif char == "p":
            return self.extract_tile(5, 4)
        elif char == "c":
            return self.extract_tile(7, 4)
        elif char == "o":
            return self.extract_tile(3, 6)
        elif char == "s":
            return self.extract_tile(1, 5)
        elif char == "B":
            return self.extract_tile(7, 10)
        elif char == "e":
            return self.extract_tile(1, 11)
        elif char == "a":
            return self.extract_tile(1, 12)


        else:
            return self.extract_tile(1, 2)

    def prepare_map(self):
        """prepares the entire image as a big numpy array"""
        for row, line in enumerate(self.contents):
            for col, char in enumerate(line):
                bm = self.get_tile(char)
                y = row*TILE_SIZE
                x = col*TILE_SIZE
                self.image[y:y+TILE_SIZE, x:x+TILE_SIZE] = bm

    def draw(self, frame):
        """
        draws the image into a frame
        """
        frame[0:self.image.shape[0], 0:self.image.shape[1]] = self.image

    def write_image(self, filename):
        """writes the image into a file"""
        cv2.imwrite(filename, self.image)



class Customer:
    def __init__(self, supermarket, avatar, row, col):
        """
        supermarket: A SuperMarketMap object
        avatar : a numpy array containing a 32x32 tile image
        row: the starting row
        col: the starting column
        """
        self.supermarket = supermarket
        self.avatar = avatar
        self.row = row
        self.col = col

    def draw(self, avatar):
        x = self.col * TILE_SIZE
        y = self.row * TILE_SIZE
#        avatar[y:y+TILE_SIZE, x:x+TILE_SIZE] = self.avatar # simple creation of the avatar
        if x > 0 & x < 13:
            if y > 0 & y < 19: ### check if coordinates are on the map
                avatar[y:y+TILE_SIZE, x:x+TILE_SIZE] = self.avatar
            else:
                cv2.destroyWindow('customer')


        self.next_minute()

    def next_minute(self):
        """propagates all customers to the next state.
        """
        self.row = self.row -1
        self.col = self.col
        return None
#    def __repr__(self):
#        return f"Customer {self.id}, is in {self.row} / {self.col}."



if __name__ == "__main__":

    background = np.zeros((384, 576, 3), np.uint8)
    tiles = cv2.imread("tiles.png")

    market = SupermarketMap(MARKET, tiles)
    customer = Customer(market, tiles[8*32:9*TILE_SIZE, 2*32:3*TILE_SIZE], 11, 15)

    while True:
        frame = background.copy()
        market.draw(frame)
        customer.draw(frame)

        # https://www.ascii-code.com/
        key = cv2.waitKey(100)
       
        if key == 113: # 'q' key
            break
    
        cv2.imshow("frame", frame)


    cv2.destroyAllWindows()

    market.write_image("supermarket.png")

