from mesa import Agent
import random
from .route import get_attraction_coordinates, Route

WIDTH = 36
HEIGHT = 36
RADIUS = 15
NUM_OBSTACLES = 80
MEMORY = 5


class Attraction(Agent):
    def __init__(self, unique_id, model, waiting_time, customer_capacity, pos, name, N_cust, heading=(1, 0)):
        super().__init__(unique_id, model)
        self.name = name
        self.pos = pos
        self.model = model
        self.waiting_time = waiting_time
        self.attraction_duration = 10
        self.current_waitingtime = 0
        self.N_current_cust = 0
        self.cust_capacity = customer_capacity
        self.cust_in_attr = 0
        self.cust_in_line = 0
        self.memory = []
        self.ride_time = 0

    def calculate_waiting_time(self):
        '''
        Calculates and updates current waiting_time of the attraction.

        TODO
        Every step that a customer is in an attraction (for a period of attraction_duration),
        waitingtime has to decrease by 1.
        '''

        # PSEUDOCODE:
        # Elke stap dat een customer aan het wachten is moet de wachttijd afnemen

        # 1. Check voor elke attractie wat de wachttijd is.
        # 2. Als de wachttijd groter is dan 1, laat de wachttijd elke stap afnemen.

        waitingtime = (self.N_current_cust * self.attraction_duration) - self.ride_time
        self.current_waitingtime = waitingtime

        if self.unique_id == 0:
            print("-------------------------------------")
            print("id: ", self.unique_id)
            print("ride time: ", self.ride_time)
            print("current cust: ", self.N_current_cust)
            print("attraction duration: ", self.attraction_duration)
            print("current_waitingtime: ", self.current_waitingtime)

    def update_memory(self):
        """
        Updates the memory of the waitingtimes of the last MEMORY timesteps
        """
        self.memory.append(self.current_waitingtime)
        if len(self.memory) == MEMORY + 1:
            self.memory.remove(self.memory[0])

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
        """step"""

        self.calculate_waiting_time()
