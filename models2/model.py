from mesa import Model, Agent
from mesa.space import SingleGrid
from mesa.space import MultiGrid
from mesa.time import RandomActivation, BaseScheduler
from mesa.datacollection import DataCollector
from collections import Counter
import matplotlib.pylab as plt
import random
import numpy as np
from .route import get_coordinates, get_attraction_coordinates, Route
from .customer import Customer
from .attraction import Attraction

WIDTH = 36
HEIGHT = 36
RADIUS = 15
NUM_OBSTACLES = 5
NUM_ATTRACTIONS = 5
waiting_times = [5.0, 5.0, 5.0, 5.0, 5.0]


x_list, y_list, positions = get_attraction_coordinates(WIDTH, HEIGHT, NUM_ATTRACTIONS)

# positions = [(1, int(HEIGHT/2)), (int(WIDTH/2), HEIGHT-1), (WIDTH-1, int(HEIGHT/2))]
starting_positions = [[int((WIDTH/2)-1), 0], [int(WIDTH/2), 0], [int((WIDTH/2)+1), 0]]
mid_point = (WIDTH/2, HEIGHT/2)


path_coordinates = get_coordinates(WIDTH, HEIGHT, NUM_OBSTACLES, NUM_ATTRACTIONS)


class Themepark(Model):
    def __init__(self, N_attr, N_cust, width, height):
        self.N_attr = N_attr    # num of attraction agents
        self.N_cust = N_cust    # num of customer agents
        self.width = width
        self.height = height

        self.grid = MultiGrid(width, height, torus=False)
        print(self.grid)
        self.schedule = BaseScheduler(self)

        self.attractions = self.make_attractions()
        self.make_attractions()
        self.make_route()
        self.add_customers()

        self.running = True


    def make_attractions(self):
        """ Initialize attractions on fixed position."""
        attractions = {}
        for i in range(self.N_attr):
            pos = (x_list[i], y_list[i])

            if self.grid.is_cell_empty(pos):
                print("Creating ATTRACTION agent {2} at ({0}, {1})"
                      .format(x_list[i], y_list[i], i))

                # TODO vet leuke namen verzinnen voor de attracties
                name = str(i)
                a = Attraction(i, self, waiting_times[i], pos, name, self.N_cust)
                attractions[i] = a
                print(a.waiting_time, "waitingtime")
                self.schedule.add(a)
                self.grid.place_agent(a, pos)
        return attractions

    def get_attractions(self):
        """
        Get a list with all attractions
        """
        agents = self.grid.get_neighbors(
            mid_point,
            moore=True,
            radius=RADIUS,
            include_center=True)

        attractions = []
        for agent in agents:
            if type(agent) == Attraction:
                attractions.append(agent)

        return attractions

    def add_customers(self):
        """ Initialize customers on random positions."""

        for i in range(self.N_cust):

            pos_temp = random.choice(starting_positions)
            rand_x = pos_temp[0]
            rand_y = pos_temp[1]

            pos = (rand_x, rand_y)

            print("Creating CUSTOMER agent {2} at ({0}, {1})"
                  .format(rand_x, rand_y, i))
            a = Customer(i, self, pos, x_list, y_list, positions)
            self.schedule.add(a)

            self.grid.place_agent(a, pos)

    def calculate_people(self):
        """Calculate how many customers are in which attraction."""

        counter_total = {}

        for attraction_pos in positions:

            agents = self.grid.get_neighbors(
                attraction_pos,
                moore=True,
                radius=0,
                include_center=True
            )

            counter = 0
            for agent in agents:
                if type(agent) is Customer:
                    counter += 1

            counter_total[attraction_pos] = counter

        return list(counter_total.values())

    def get_durations(self):
        """ Get duraction of every attraction in a list """

        durations = []

        for attraction_pos in positions:

            agents = self.grid.get_neighbors(
                attraction_pos,
                moore=True,
                radius=0,
                include_center=True
            )

            for agent in agents:
                if type(agent) is Attraction:
                    durations.append(agent.attraction_duration)

        return durations

    def make_route(self):
        """Draw coordinates of a possible path."""

        for i in range(len(path_coordinates)):
            pos = path_coordinates[i]

            if pos not in positions:

                # Create path agent
                path = Route(i, self, pos)
                self.schedule.add(path)

                self.grid.place_agent(path, pos)

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()