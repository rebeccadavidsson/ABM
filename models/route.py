from mesa import Agent
import numpy as np
import random

WIDTH = 36
HEIGHT = 36
starting_positions = [[int((WIDTH/2)-1), 0], [int(WIDTH/2), 0], [int((WIDTH/2)+1), 0]]


class Route(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.model = model


def get_coordinates(width, height, num_obstacles, num_attractions):
    """Calculate the coordinates of a route, given the
    width and height of a grid."""

    coordinates = []

    positions = get_attraction_coordinates(width, height, num_attractions)[2]

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


def get_attraction_coordinates(width, height, num_attractions):
    """Generate random coordinates for attractions."""
    # TODO: minder random, checken dat ze niet te dicht bij elkaar mogen.

    xlist, ylist, total = [], [], []

    for i in range(num_attractions):
        xlist.append(random.randrange(0, width))
        ylist.append(random.randrange(10, height))

    for i in range(num_attractions):
        total.append((xlist[i], ylist[i]))

    return xlist, ylist, total
