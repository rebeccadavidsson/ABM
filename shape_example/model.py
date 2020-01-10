from mesa import Model, Agent
from mesa.space import SingleGrid
from mesa.time import RandomActivation


class Walker(Agent):
    def __init__(self, unique_id, model, pos, heading=(1, 0)):
        super().__init__(unique_id, model)
        self.pos = pos
        self.heading = heading
        self.headings = {(1, 0), (0, 1), (-1, 0), (0, -1)}


class Attraction(Model):
    def __init__(self, N=2, width=20, height=10):
        self.N = N    # num of agents
        self.headings = ((1, 0), (0, 1), (-1, 0), (0, -1))  # tuples are fast
        self.grid = SingleGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)
        self.make_walker_agents()
        self.running = True

    def make_walker_agents(self):
        positions = [(1, 15), (10, 25)]
        x_list = [0, 10, 24]
        y_list = [10, 19, 10]
        for i in range(self.N):

            heading = (1, 0)
            pos = (x_list[i], y_list[i])

            print(pos, "XY")
            # heading = self.random.choice(self.headings)
            # heading = (1, 0)
            if self.grid.is_cell_empty(pos):
                print("Creating agent {2} at ({0}, {1})"
                      .format(x_list[i], y_list[i], i))
                a = Walker(i, self, pos, heading)
                self.schedule.add(a)
                self.grid.place_agent(a, pos)



    def step(self):
        self.schedule.step()
