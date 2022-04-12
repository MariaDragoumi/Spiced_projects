import numpy as np
import time
from faker import Faker
import cv2
import algoritm_moves
import random

# Global variables
TILE_SIZE = 32
background = np.zeros((384, 576, 3), np.uint8)
tiles = cv2.imread("tiles2.png")

MARKET = """
######44##########
##..............##
#5..94..1k..de..B#
#5..94..2l..fs..o#
#6..83..3n..hg..a#
#6..82..4q..im..c#
#7..71..1r..jb..p#
##..............##
##..C#..C#..C#..##
##..##..##..##..##
##..............##
######GG######GG##
""".strip()

grid = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
    [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
    [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
    [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
    [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
    [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1],
])
station_locs = {
    'fruits': (6, 15),
    'spices': (6, 11),
    'drinks': (6, 7),
    'dairy': (6, 3),
    'checkout': (8, 7),
    }
# The order is: dairy, spices, drink, fuits, checkout, entry
transition_matrix = np.array([
    [0.73733108, 0.05140766, 0.05861486, 0.04988739, 0.10275901, 0],
    [0.19336840, 0.40235932, 0.16323928, 0.09102503, 0.15000797, 0],
    [0.01090086, 0.08700123, 0.59862197, 0.08792678, 0.21554916, 0],
    [0.09597669, 0.05070467, 0.05487757, 0.59727581, 0.20116526, 0],
    [0.00000000, 0.00000000, 0.00000000, 0.00000000, 1.00000000, 0],
    [0.28744100, 0.18133000, 0.15339200, 0.37730000, 0.00053700, 0],
    ])
entry_probs = {
    0: 0.4006741573033708,
    1: 0.16157303370786516,
    2: 0.14449438202247192,
    3: 0.12,
    4: 0.07460674157303371,
    5: 0.05393258426966292,
    6: 0.027640449438202246,
    7: 0.010786516853932584,
    8: 0.004044943820224719,
    9: 0.0020224719101123597,
    11: 0.00022471910112359551,
    }


class SupermarketMap:
    """
    Visualizes the supermarket background
    """
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

# adding fruits
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
# adding spices
        elif char == "d":
            return self.extract_tile(1, 8)
        elif char == "f":
            return self.extract_tile(1, 10)
        elif char == "h":
            return self.extract_tile(2, 8)
        elif char == "i":
            return self.extract_tile(0, 10)
        elif char == "j":
            return self.extract_tile(3, 8)
        elif char == "k":
            return self.extract_tile(6, 8)
        elif char == "l":
            return self.extract_tile(0, 11)
        elif char == "n":
            return self.extract_tile(0, 7)
        elif char == "q":
            return self.extract_tile(1, 7)
        elif char == "r":
            return self.extract_tile(6, 3)
# adding drinks
        elif char == "1":
            return self.extract_tile(4, 9)
        elif char == "2":
            return self.extract_tile(5, 9)
        elif char == "3":
            return self.extract_tile(6, 9)
        elif char == "4":
            return self.extract_tile(3, 13)
# adding dairy
        elif char == "5":
            return self.extract_tile(0, 3)
        elif char == "6":
            return self.extract_tile(4, 5)
        elif char == "7":
            return self.extract_tile(5, 6)
        elif char == "8":
            return self.extract_tile(6, 6)
        elif char == "9":
            return self.extract_tile(0, 13)
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


class Customer():
    """
    a single customer that moves through the supermarket
    in a MCMC simulation
    """
    def __init__(self, name, state, transition_matrix,
                 supermarket, avatar, row, col):
        self.name = name
        self.state = state
        self.transition_probs = transition_matrix
        self.supermarket = supermarket
        self.avatar = avatar
        self.row = row
        self.col = col
        self.path = []
        self.step_counter = 0

    def __repr__(self):
        return f'{self.name} is in {self.state}'

    def next_state(self):
        '''
        Propagates the customer to the next state.
        Returns nothing.
        '''
        state_dict = {
            'dairy': 0,
            'spices': 1,
            'drinks': 2,
            'fruits': 3,
            'checkout': 4,
            'entry': 5
            }
        self.state = np.random.choice(
            ['dairy', 'spices', 'drinks', 'fruits', 'checkout', 'entry'],
            p=self.transition_probs[state_dict[f'{self.state}']]
            )

    def is_active(self):
        """
        Returns True if the customer has not reached the checkout yet.
        """
        active = self.state != 'checkout'
        return active

    def draw(self, frame):
        x = self.col*TILE_SIZE
        y = self.row*TILE_SIZE

        frame[y:y+TILE_SIZE, x:x+TILE_SIZE] = self.avatar
        if x > 0 & x < 13:
            if y > 0 & y < 19:  # check if coordinates are on the map
                frame[y:y+TILE_SIZE, x:x+TILE_SIZE] = self.avatar
            else:
                cv2.destroyWindow('customer')

        if self.step_counter < len(self.path):
            next_step = self.path[self.step_counter]
            self.next_position(next_step)
        else:
            last_step = self.path[-1]
            self.next_position(last_step)
        self.step_counter += 1

    def get_path(self):
        destination = (
            np.add(
                station_locs[self.state],
                (
                    np.random.choice([-4, -3, -2, -1, 0]),
                    np.random.choice([-1, 0])
                    )
                )
            )
        start_given = (self.row, self.col)  # current state
        finish_given = destination
        possible_moves = [(0, 1), (0, -1), (1, 0), (-1, 0),
                          (1, 1), (1, -1), (-1, 1), (-1, -1)]
        path = algoritm_moves.find_path(grid, start_given,
                                        finish_given, possible_moves)
        self.path = path
        self.step_counter = 0

    def next_position(self, step):
        """
        propagates all customers to the next state.
        """
        self.row = step[0]  # Stay!
        self.col = step[1]  # Stay!
        return None

    def position(self):
        return f"Customer {self.name}, is in {self.row} / {self.col}."


class Supermarket:
    """
    Manages multiple Customer instances that are currently in the market.
    """
    def __init__(self, market_map):
        self.customers = {}
        self.minutes = 0
        self.last_id = 0
        self.market_map = market_map

    def __repr__(self):
        return f'Supermarket customers: {len(self.customers)}, \
                  Time: {self.minutes}, Last customer ID: {self.last_id}'

    def get_time(self):
        """
        Current time in HH:MM format,
        """
        return self.minutes

    def add_new_customers(self):
        """
        Randomly creates new customers.
        """
        entry_no = np.random.choice(
            list(entry_probs.keys()),
            p=list(entry_probs.values())
            )
        entrance = [(7, 14), (7, 15), (8, 14), (8, 15),
                    (9, 14), (9, 15), (10, 14), (10, 15)]
        entry_position = random.choice(entrance)
        for _ in range(entry_no):
            random_x = np.random.choice([3, 4, 5, 6])
            avatar = tiles[8*32:9*TILE_SIZE,
                           random_x*32:(random_x+1)*TILE_SIZE]
            self.last_id += 1
            entry_point = 'entry'
            f = Faker()
            name = f.name()
            customer = Customer(
                name,
                entry_point,
                transition_matrix,
                self.market_map,
                avatar,
                entry_position[0],
                entry_position[1]
                )
            self.customers.update({self.last_id: customer})
            print(f'{customer.name} entered the supermarket')
        return None

    def move_customers(self):
        """
        Move all customers randomly.
        """
        for _, customer in self.customers.items():
            customer.next_state()
            customer.get_path()

    def print_customers(self):
        """
        Print all customers with the current time and id in CSV format.
        """
        for _, customer in list(self.customers.items()):
            print(customer)
        return None

    def remove_exitsting_customers(self):
        """
        Removes every customer that is not active any more.
        """
        for key, customer in list(self.customers.items()):
            if not customer.is_active():
                del self.customers[key]
        return None

    def next_minute(self):
        """
        Propagates all customers to the next state.
        """
        self.minutes += 1
        self.remove_exitsting_customers()
        self.add_new_customers()
        self.move_customers()
        self.print_customers()
        print(f'--> Minutes: {self.minutes}, \
            last ID: {self.last_id}, \
            customers inside: {len(self.customers)}')


if __name__ == "__main__":
    i = 0
    market = SupermarketMap(MARKET, tiles)
    DOODL = Supermarket(market)
    DOODL.next_minute()

    while True:
        i = i+1
        frame = background.copy()
        market.draw(frame)
        for key, customer in list(DOODL.customers.items()):
            customer.draw(frame)
        print(f"step: {i}")
        # https://www.ascii-code.com/
        key = cv2.waitKey(20)
        if key == 113:  # 'q' key
            break
        cv2.imshow("frame", frame)
        if i == 1:
            time.sleep(2)
        if not i % 25:
            DOODL.next_minute()
        DOODL.print_customers()
        if i == 201:
            break
        market.write_image("supermarket.png")
        """
        starts at 1, otherwise it creates a blank (black) frame at the start
        only saves the images if there is the folder
        """
        if i > 0:
            cv2.imwrite('frames/supermarket'+str(i)+'.png', frame)

    cv2.destroyAllWindows()

    market.write_image("supermarket.png")
