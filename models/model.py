from mesa import Model, Agent
from mesa.space import SingleGrid
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from collections import Counter
import matplotlib.pylab as plt
import random
import numpy as np

x_list = [0, 13, 25]
y_list = [13, 25, 13]
positions = [(0,13), (13,25), (25, 13)]
num_people = 100
heading = (1, 0)


class Customer(Agent):
    def __init__(self, unique_id, model, pos, heading=(1, 0)):
        super().__init__(unique_id, model)
        self.pos = pos
        self.model = model
        self.heading = heading
        self.headings = {(1, 0), (0, 1), (-1, 0), (0, -1)}

    def random_move(self):
        neigh_cells = self.model.grid.get_neighborhood(self.pos, True)
        # print("neighborhood: ", neigh_cells)
        selected_cell = neigh_cells[0]
        self.model.grid.move_agent(self, selected_cell)

    def step(self):
        # The agent's step will go here.
        # self.random_move()
        pass


class Attraction(Agent):
    def __init__(self, unique_id, model, pos, heading=(1, 0)):
        super().__init__(unique_id, model)
        self.pos = pos
        self.model = model
        self.heading = heading
        self.headings = {(1, 0), (0, 1), (-1, 0), (0, -1)}

    def step(self):
        # The agent's step will go here.
        pass


class Themepark(Model):
    def __init__(self, N_attr, N_cust, width, height):
        self.N_attr = N_attr    # num of attraction agents
        self.N_cust = N_cust    # num of customer agents
        self.width = width
        self.height = height

        self.headings = ((1, 0), (0, 1), (-1, 0), (0, -1))

        self.grid = MultiGrid(width, height, torus=False)

        # Dit onderscheid is waarschijnlijk niet nodig, maar werd zo gedaan in wolf/sheep dus even testen
        self.schedule_Customer = RandomActivation(self)
        self.schedule_Attraction = RandomActivation(self)

        self.datacollector = DataCollector(
            {"Customer": lambda m: self.schedule_Customer.get_agent_count(),
            "Attraction": lambda m: self.schedule_Attraction.get_agent_count()})

        self.make_attractions()
        self.add_customers()
        # self.add_people()

        self.running = True
        self.datacollector.collect(self)

    def make_attractions(self):
        """ Initialize attractions on fixed position."""

        for i in range(self.N_attr):
            pos = (x_list[i], y_list[i])

            if self.grid.is_cell_empty(pos):
                print("Creating ATTRACTION agent {2} at ({0}, {1})"
                      .format(x_list[i], y_list[i], i))
                a = Attraction(i, self, pos, heading)
                self.schedule_Attraction.add(a)
                self.grid.place_agent(a, pos)

    def add_customers(self):
        """ Initialize customers on random positions."""

        for i in range(self.N_cust):
            rand_x = random.choice(list(np.arange(0, self.width)))
            rand_y = random.choice(list(np.arange(0, self.height)))
            pos = (rand_x, rand_y)

            print("Creating CUSTOMER agent {2} at ({0}, {1})"
                  .format(rand_x, rand_y, i))
            a = Customer(i, self, pos, heading)
            self.schedule_Customer.add(a)
            self.grid.place_agent(a, pos)

    def add_people(self):
        """Add people to a random attraction."""

        position_counter = []
        for person in range(num_people):

            # Go to random attraction
            pos = random.choice(positions)
            position_counter.append(pos)

            # Make individual agents
            customer = Customer(person, self, pos, heading)
            self.grid.place_agent(customer, pos)

        # Calculate how many customers are where
        count = [[x, position_counter.count(x)] for x in set(position_counter)]

        x = []
        for i in count:
            x.append(i[1])

        y_pos = ['Attraction1','Attraction2','Attraction3']
        plt.bar(y_pos, x, align='center', alpha=0.5)
        plt.xticks([0,1,2], y_pos)

        plt.show()

    def step(self):
        """Advance the model by one step."""
        # self.schedule_Customer.step()
        # self.schedule_Attraction.step()
        #
        # self.datacollector.collect(self)
        pass
