from mesa import Agent
import random
from .route import get_coordinates


WIDTH = 26
HEIGHT = 26

path_coordinates = get_coordinates(WIDTH, HEIGHT)

x_list = [1, int(WIDTH/2), WIDTH-1]
y_list = [int(HEIGHT/2), HEIGHT-1, int(HEIGHT/2)]
positions = [(1, int(HEIGHT/2)), (int(WIDTH/2), HEIGHT-1), (WIDTH-1, int(HEIGHT/2))]


class Attraction(Agent):
    def __init__(self, unique_id, model, waiting_time, pos, name, N_cust, heading=(1, 0)):
        super().__init__(unique_id, model)
        self.name = name
        self.pos = pos
        self.model = model

        # self.waiting_time = random.randrange(10, 20)
        self.waiting_time = waiting_time
        self.attraction_duration = 10
        self.max_queue = int(N_cust * 2)
        self.N_current_cust = 0
