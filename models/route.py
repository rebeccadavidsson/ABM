from mesa import Agent
import numpy as np
import random
import math

WIDTH = 36
HEIGHT = 36
starting_positions = [[int((WIDTH/2)-1), 0], [int(WIDTH/2), 0], [int((WIDTH/2)+1), 0]]


class Route(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.model = model


def get_coordinates(width, height, num_obstacles, num_attractions, method):
    """Calculate the coordinates of a route, given the
    width and height of a grid."""

    coordinates = []

    positions = get_attraction_coordinates(width, height, num_attractions, method)[2]

    for i in range(num_obstacles):
        coordinate = (random.randrange(width), random.randrange(height))

        # TODO: checken of het overlapt met andere agents
        while coordinate in positions or coordinate in starting_positions:
            coordinate = (random.randrange(width), random.randrange(height))

        coordinates.append((random.randrange(width), random.randrange(height)))

    # Hardcode starting path
    coordinates.append((int((WIDTH/2) - 2), 0))
    coordinates.append((int((WIDTH/2) - 2), 1))
    coordinates.append((int((WIDTH/2) + 2), 0))
    coordinates.append((int((WIDTH/2) + 2), 1))
    return coordinates


def get_attraction_coordinates(width, height, num_attractions, method):
    """Generate random coordinates for attractions."""
    # TODO: minder random, checken dat ze niet te dicht bij elkaar mogen.
    xlist, ylist, total = [], [], []

    if method == "random":

        for i in range(num_attractions):
            xlist.append(random.randrange(0, width))
            ylist.append(random.randrange(10, height))

        for i in range(num_attractions):
            total.append((xlist[i], ylist[i]))

    elif method == "circle":
        r = width / 3
        total = calc_points(r, num_attractions, WIDTH, HEIGHT)
        print(total)
        for i in total:
            xlist.append(i[0])
            ylist.append(i[1])

    return xlist, ylist, total


def calc_points(r, n, WIDTH, HEIGHT):
    print()
    return [(int(math.cos(2* np.pi/n*x)*r) + int(WIDTH / 2), int(math.sin(2* np.pi/n*x)*r) + int(HEIGHT / 2)) for x in range(0, n+10)]
