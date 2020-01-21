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
NUM_OBSTACLES = 0
NUM_ATTRACTIONS = 7
RADIUS = int(WIDTH/2)


x_list, y_list, positions = get_attraction_coordinates(WIDTH, HEIGHT, NUM_ATTRACTIONS)
starting_positions = [[int((WIDTH/2)-1), 0], [int(WIDTH/2), 0], [int((WIDTH/2)+1), 0]]
mid_point = (int(WIDTH/2), int(HEIGHT/2))


path_coordinates = get_coordinates(WIDTH, HEIGHT, NUM_OBSTACLES, NUM_ATTRACTIONS)

waiting_times = [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0]
customer_capacity = [5, 5, 5, 5, 5, 5, 5]

class Themepark(Model):
    def __init__(self, N_attr, N_cust, width, height, Strategy):

        self.N_attr = N_attr    # num of attraction agents
        self.N_cust = N_cust    # num of customer agents
        self.width = width
        self.height = height
        self.total_steps = 0
        self.cust_ids = N_cust

        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = BaseScheduler(self)
        self.schedule_Attraction = BaseScheduler(self)
        self.schedule_Customer = BaseScheduler(self)

        self.attractions = self.make_attractions()
        self.make_attractions()
        self.make_route()
        self.add_customers(self.N_cust)

        self.running = True
        self.datacollector = DataCollector(
            # {"Custumors": lambda m: self.schedule_Customer.get_agent_count(),
            #  "Attractions": lambda m: self.schedule_Attraction.get_agent_count()})
            {"Attraction1": lambda m: self.schedule_Attraction.agents[0].customers_inside(),
            "Attraction2": lambda m: self.schedule_Attraction.agents[1].customers_inside(),
            "Attraction3": lambda m: self.schedule_Attraction.agents[2].customers_inside()
            })

        self.total_waited_time = 0

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
                a = Attraction(i, self, waiting_times[i], customer_capacity[i], pos, name, self.N_cust)
                attractions[i] = a
                print(a.waiting_time, "waitingtime")
                self.schedule_Attraction.add(a)
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

    def add_customers(self, N_cust, added=False):
        """ Initialize customers on random positions."""

        for i in range(N_cust):

            pos_temp = random.choice(starting_positions)
            rand_x, rand_y = pos_temp[0], pos_temp[1]

            pos = (rand_x, rand_y)

            print("Creating CUSTOMER agent {2} at ({0}, {1})"
                  .format(rand_x, rand_y, i))
            if added is True:
                i = self.cust_ids
            a = Customer(i, self, pos, x_list, y_list, positions)
            self.schedule_Customer.add(a)

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
                else:
                    attraction = agent

            attraction.N_current_cust = counter
            counter_total[attraction_pos] = counter

        return list(counter_total.values())

    def calculate_people_sorted(self):
        """
        Calculate how many customers are in which attraction.
        Returns a SORTED LIST.
        For example: indexes = [3, 2, 5, 1, 4]
        indicates that attraction3 has the least people waiting.
        """

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
                else:
                    attraction = agent

            attraction.N_current_cust = counter
            counter_total[attraction.unique_id] = counter

        # TODO, dit moet nog uitgebreid worden naar als er bijvorobeeld 3
        # wachttijden gelijk zijn. Nu wordt alleen gecheckt of wachttijden
        # bijvorobeeld overal 10 zijn of overal 0, dus overal gelijk.

        # dit is altijd true want dict keys worden meegenomen bij dict.items() en die zijn nooit verschillend (dus set nemen verandert niets)
        if len(counter_total.items()) == len(set(counter_total.items())):
            a1 = list(counter_total.items())
            # print("A11111111111111111111111111111", a1.values())
            random.shuffle(a1)
            print(a1)
            counter_total = dict(a1)
            print(counter_total)

        # if len(counter_total.values()) != len(set(counter_total.values())):



        # indexes = []
        # {indexes.append(k): v for k, v in sorted(counter_total.items(), key=lambda item: item[1])}

        return counter_total

    def get_durations(self):
        """ Get duratiosn of every attraction in a list """

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
        self.datacollector.collect(self)
        self.schedule_Attraction.step()
        self.schedule_Customer.step()

        # update memory of attractions
        attractions = self.get_attractions()
        for attraction in attractions:
            attraction.update_memory()

        self.total_steps += 1

        if self.total_steps > random.randrange(10, 20) and self.cust_ids < self.N_cust * 2:
            self.cust_ids += 1
            self.add_customers(1, added=True)
            self.total_steps = 0
