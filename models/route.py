
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
