from mesa import Agent
import numpy as np

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
        coordinates.append((i, int(temp / 2)))
        coordinates.append((i, int(temp / 2) + 1))
        coordinates.append((i, int(temp / 2) - 1))
        coordinates.append((int(temp / 2), i))
        coordinates.append((int(temp / 2) + 1, i))
        coordinates.append((int(temp / 2) - 1, i))
        temp += 1
    #
    # een extra comment omdat ik antwoord wil geven op de commit vraag
    # POGING TOT EEN ROUTE-ALGORITME
    # grid_matrix = np.zeros((5, 5))
    # for i in range(5):
    #
    #     temp = 5
    #     grid_matrix[int(temp/2), i] = 1
    #     grid_matrix[int(temp / 2) + 1,i ] = 1
    #     # grid_matrix[int(temp / 2) - 1,i ] = 1
    #     grid_matrix[i, int(temp / 2)] = 1
    #     grid_matrix[i, int(temp / 2) + 1] = 1
    #     # grid_matrix[i, int(temp / 2) - 1] = 1
    #     temp += 1
    # print(grid_matrix)
    #
    # attractions = [(0,3), (3,0), (3,5)]
    # middle = (3,3)

    # routes_dict = {}
    # for i in range(len(attractions)):
    #     routes_dict[i] = {}
    #     for j in range(len(attractions)):
    #         routes_dict[i][j] = []
    # print(routes_dict)
    #
    # current_location = None
    # find_route = {}
    # for attr in attractions:
    #     current_location = attr
    #
    #     while current_location is not middle:
    #         for i in range(8):
    #
    #             try:
    #                 if grid_matrix[current_location[0]+1][current_location[1]] is not 0:
    #                 find_route[current_location] = grid_matrix[current_location[0]+1][current_location[1]]
    #             except:
    #                 None
    #
    #             try:
    #                 if grid_matrix[current_location[0]+1][current_location[1]] is not 0:
    #                     find_route[current_location] = grid_matrix[current_location[0]][current_location[1]+1]
    #             except:
    #                 None
    #
    #             try:
    #                 if grid_matrix[current_location[0]+1][current_location[1]] is not 0:
    #                     find_route[current_location] = grid_matrix[current_location[0]-1][current_location[1]]
    #             except:
    #                 None
    #
    #             try:
    #                 if grid_matrix[current_location[0]+1][current_location[1]] is not 0:
    #                     find_route[current_location]= grid_matrix[current_location[0]][current_location[1]-1]
    #             except:
    #                 None
    #

    return coordinates
