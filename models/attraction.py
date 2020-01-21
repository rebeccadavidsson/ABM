from mesa import Agent
import random
from .route import get_attraction_coordinates, Route

WIDTH = 36
HEIGHT = 36
RADIUS = 15
NUM_OBSTACLES = 80


class Attraction(Agent):
    def __init__(self, unique_id, model, waiting_time, customer_capacity, pos, name, N_cust, heading=(1, 0)):
        super().__init__(unique_id, model)
        self.name = name
        self.pos = pos
        self.model = model
        self.waiting_time = waiting_time
        self.attraction_duration = 10
        self.max_queue = int(N_cust * 2)

        # TODO: current_waitingtime moet worden geupdated in customer.py
        self.current_waitingtime = 0
        self.N_current_cust = 1

        self.cust_capacity = customer_capacity
        self.cust_in_attr = 0
        self.cust_in_line = 0


    def calculate_waiting_time(self):
        '''
        Calculates current waiting_time of the attraction
        '''
        waitingtime = self.N_current_cust * self.attraction_duration
        self.current_waitingtime = waitingtime


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

    # def step(self):
