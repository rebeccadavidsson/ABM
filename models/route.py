from mesa import Agent


class Route(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.model = model


def get_coordinates(width, height):
    """Calculate the coordinates of a route, given the
    width and height of a grid."""

    coordinates = []

    for i in range(width):

        temp = width
        coordinates.append([i, int(temp / 2)])
        coordinates.append([i, int(temp / 2) + 1])
        coordinates.append([i, int(temp / 2) - 1])
        coordinates.append([int(temp / 2), i])
        coordinates.append([int(temp / 2) + 1, i])
        coordinates.append([int(temp / 2) - 1, i])
        temp += 1

    return coordinates
