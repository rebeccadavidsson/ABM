from mesa import Model, Agent
from mesa.space import SingleGrid
from mesa.time import RandomActivation

x_list = [0, 13, 25]
y_list = [13, 25, 13]
num_people = 100


class Custumor(Agent):
    def __init__(self, unique_id, model, pos, heading=(1, 0)):
        super().__init__(unique_id, model)
        self.pos = pos
        self.heading = heading
        self.headings = {(1, 0), (0, 1), (-1, 0), (0, -1)}


class Themepark(Agent):
    def __init__(self, unique_id, model, pos, heading=(1, 0)):
        super().__init__(unique_id, model)
        self.pos = pos
        self.heading = heading
        self.headings = {(1, 0), (0, 1), (-1, 0), (0, -1)}


class ThemeparkGrid(Model):
    def __init__(self, N=2, width=20, height=10):
        self.N = N    # num of agents
        self.headings = ((1, 0), (0, 1), (-1, 0), (0, -1))
        self.grid = SingleGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)
        self.make_attractions()
        self.running = True
        self.add_people()

    def make_attractions(self):

        for i in range(self.N):

            heading = (1, 0)
            pos = (x_list[i], y_list[i])

            if self.grid.is_cell_empty(pos):
                print("Creating agent {2} at ({0}, {1})"
                      .format(x_list[i], y_list[i], i))
                a = Themepark(i, self, pos, heading)
                self.schedule.add(a)
                self.grid.place_agent(a, pos)

    def add_people(self):

        for person in range(num_people):

            # Go to random

            # TODO

            # Make individual agents
            # custumor = Custumor(person, self, pos, heading)

            pass
        pass
