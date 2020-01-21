from mesa import Agent
import random
from .route import get_coordinates, Route
from . import *
# from .customer import Customer


WIDTH = 26
HEIGHT = 26

path_coordinates = get_coordinates(WIDTH, HEIGHT)

x_list = [1, int(WIDTH/2), WIDTH-1]
y_list = [int(HEIGHT/2), HEIGHT-1, int(HEIGHT/2)]
positions = [(1, int(HEIGHT/2)), (int(WIDTH/2), HEIGHT-1), (WIDTH-1, int(HEIGHT/2))]


class Attraction(Agent):
    def __init__(self, unique_id, model, waiting_time, customer_capacity, pos, name, N_cust, heading=(1, 0)):
        super().__init__(unique_id, model)
        self.name = name
        self.pos = pos
        self.model = model
        self.waiting_time = waiting_time
        self.attraction_duration = 10
        self.max_queue = int(N_cust * 2)

        self.cust_capacity = customer_capacity
        self.cust_in_attr = 0
        self.cust_in_line = 0

    def customers_inside(self):
        """Determine the amount of customers inside the Attraction agent."""

        # Get all agents at attraction location
        agents = self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            radius=0,
            include_center=True
        )

        # Count customer agents
        counter = 0
        for agent in agents:

            if type(agent) != Route and type(agent) != Attraction:
                counter += 1

        return counter

    def run_attraction(self, amount):
        """Customers enter attraction and leave waiting line."""
        
        self.cust_in_attr = amount
        self.cust_in_line -= amount

    def step(self):
