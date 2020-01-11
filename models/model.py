from mesa import Model, Agent
from mesa.space import SingleGrid
from mesa.space import MultiGrid
from mesa.time import RandomActivation, BaseScheduler
from mesa.datacollection import DataCollector
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import random

# x_list = [1, 2, 3]
# y_list = [1, 2, 3]
# positions = [(1,1), (2, 2), (3, 3)]

# TODO: Dit is nu gehardcode....
x_list = [1, 13, 25]
y_list = [13, 25, 13]
positions = [(1,13), (13,25), (25, 13)]



num_people = 100
heading = (1, 0)


class Custumor(Agent):
    def __init__(self, unique_id, model, pos, heading=(1, 0)):
        super().__init__(unique_id, model)
        self.pos = pos
        self.heading = heading
        self.headings = {(1, 0), (0, 1), (-1, 0), (0, -1)}


class Attraction(Agent):
    def __init__(self, unique_id, model, pos, heading=(1, 0)):
        super().__init__(unique_id, model)
        self.pos = pos
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
        print("possible", possible_steps)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        '''
        This method should move the customer using the `random_move()` method.
        '''
        print("STEPPING")
        self.move()

class Themepark(Model):
    def __init__(self, N=2, width=20, height=10):
        self.N = N    # num of agents
        self.headings = ((1, 0), (0, 1), (-1, 0), (0, -1))
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = BaseScheduler(self)
        self.make_attractions()
        self.running = True
        self.add_people()

    def make_attractions(self):
        """ Initialize attractions on fixed position."""

        for i in range(self.N):

            pos = (x_list[i], y_list[i])

            if self.grid.is_cell_empty(pos):
                print("Creating agent {2} at ({0}, {1})"
                      .format(x_list[i], y_list[i], i))
                a = Attraction(i, self, pos, heading)
                self.schedule.add(a)
                self.grid.place_agent(a, pos)

    def add_people(self):
        """Add people to a random attraction."""

        self.position_counter = []
        for person in range(num_people):

            # Go to random attraction
            pos = random.choice(positions)
            self.position_counter.append(pos)

            # Make individual agents
            custumor = Custumor(person, self, pos, heading)
            self.grid.place_agent(custumor, pos)

    def calculate_people(self):
        """Calculate how many customers are in which attraction."""
        return [[x, self.position_counter.count(x)] for x in set(self.position_counter)]

    def step(self):
        self.schedule.step()


        # x = []
        # for i in count:
        #     x.append(i[1])
        #
        # y_pos = ['Attraction1', 'Attraction2', 'Attraction3']
        # plt.bar(y_pos, x, align='center', alpha=0.5)
        # plt.xticks([0, 1, 2], y_pos)

        # plt.show()
