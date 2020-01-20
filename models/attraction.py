from mesa import Agent
import random
from .route import get_attraction_coordinates

WIDTH = 36
HEIGHT = 36
RADIUS = 15
NUM_OBSTACLES = 80
MEMORY = 5


class Attraction(Agent):
    def __init__(self, unique_id, model, pos, name, N_cust):
        super().__init__(unique_id, model)
        self.name = name
        self.pos = pos
        self.model = model

        self.current_waitingtime = 0
        self.attraction_duration = 10
        self.max_queue = int(N_cust * 2)
        self.N_current_cust = 1

        self.memory = []

    def calculate_waiting_time(self):
        '''
        Calculates current waiting_time of the attraction
        '''
        waitingtime = self.N_current_cust * self.attraction_duration
        self.current_waitingtime = waitingtime

    def update_memory(self):
        """
        Updates the memory of the waitingtimes of the last MEMORY timesteps
        """
        print("TEEEEEEEEEEEEEEEEEEEEEEEEEEEEEST")
        print(self.memory)
        self.memory.append(self.current_waitingtime)
        if len(self.memory) == MEMORY + 1:
            self.memory.remove(self.memory[0])
