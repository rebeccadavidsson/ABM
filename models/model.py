from mesa import Model, Agent
from mesa.space import SingleGrid
from mesa.space import MultiGrid
from mesa.time import RandomActivation, BaseScheduler
from mesa.datacollection import DataCollector
from collections import Counter
import matplotlib.pylab as plt
import random
import numpy as np
from .route import get_coordinates


WIDTH = 26
HEIGHT = 26

path_coordinates = get_coordinates(WIDTH, HEIGHT)

x_list = [1, int(WIDTH/2), WIDTH-1]
y_list = [int(HEIGHT/2), HEIGHT-1, int(HEIGHT/2)]
positions = [(1, int(HEIGHT/2)), (int(WIDTH/2), HEIGHT-1), (WIDTH-1, int(HEIGHT/2))]
heading = (1, 0)


class Customer(Agent):
    def __init__(self, unique_id, model, pos, heading=(1, 0)):
        super().__init__(unique_id, model)
        self.pos = pos
        self.model = model
        self.heading = heading
        self.headings = {(1, 0), (0, 1), (-1, 0), (0, -1)}

    def move(self):
        '''
        This method should get the neighbouring cells (Moore's neighbourhood),
        select one, and move the agent to this cell.
        '''
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        new_position = self.random.choice(possible_steps)

        # Restrict to path
        while list(new_position) not in path_coordinates:
            new_position = self.random.choice(possible_steps)

        self.model.grid.move_agent(self, new_position)

    def step(self):
        '''
        This method should move the customer using the `random_move()` method.
        '''
        self.move()


class Attraction(Agent):
    def __init__(self, unique_id, model, pos, name, heading=(1, 0)):
        super().__init__(unique_id, model)
        self.name = name
        self.pos = pos
        self.model = model
        self.heading = heading
        self.headings = {(1, 0), (0, 1), (-1, 0), (0, -1)}


class Themepark(Model):
    def __init__(self, N_attr, N_cust, width, height):
        self.N_attr = N_attr    # num of attraction agents
        self.N_cust = N_cust    # num of customer agents
        self.width = width
        self.height = height

        self.headings = ((1, 0), (0, 1), (-1, 0), (0, -1))

        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = BaseScheduler(self)

        self.attractions = self.make_attractions()
        self.make_attractions()
        self.make_route()
        self.add_customers()

        self.running = True
        # self.datacollector.collect(self)

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
                a = Attraction(i, self, pos, name, heading)
                attractions[i] = a
                self.schedule.add(a)
                self.grid.place_agent(a, pos)
        return attractions

    def add_customers(self):
        """ Initialize customers on random positions."""

        for i in range(self.N_cust):
            pos_temp = random.choice(path_coordinates)
            rand_x = pos_temp[0]
            rand_y = pos_temp[1]

            pos = (rand_x, rand_y)
            print("Creating CUSTOMER agent {2} at ({0}, {1})"
                  .format(rand_x, rand_y, i))
            a = Customer(i, self, pos, heading)
            self.schedule.add(a)
            self.grid.place_agent(a, pos)

    def calculate_people(self):
        """Calculate how many customers are in which attraction."""

        return [random.random(), random.random(), random.random()]

    def make_route(self):
        """Draw coordinates of a possible path."""

        for i in range(len(path_coordinates)):
            pos = path_coordinates[i]

            # Create path agent?
            path = Route(i, self, pos)
            self.schedule.add(path)
            self.grid.place_agent(path, pos)

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()


class Route(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.model = model
