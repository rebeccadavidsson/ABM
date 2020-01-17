from mesa import Agent
import random
from .route import get_attraction_coordinates

WIDTH = 36
HEIGHT = 36
RADIUS = 15
NUM_OBSTACLES = 80


class Attraction(Agent):
    def __init__(self, unique_id, model, waiting_time, pos, name, N_cust):
        super().__init__(unique_id, model)
        self.name = name
        self.pos = pos
        self.model = model

        # self.waiting_time = random.randrange(10, 20)
        # TODO: volgens mij kan waiting_time weg? Want is ook in customers en we
        # hebben ook al attraction_duration
        self.current_waitingtime = 0
        self.attraction_duration = 10
        self.max_queue = int(N_cust * 2)
        self.N_current_cust = 0

    def calculate_waiting_time(self):
        '''
        Calculates current waiting_time of the attraction
        '''
        waitingtime = self.N_current_cust * self.attraction_duration
        self.current_waitingtime = waitingtime
