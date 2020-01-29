from mesa import Model
from mesa.space import MultiGrid
from mesa.time import BaseScheduler
from mesa.datacollection import DataCollector
import random
import numpy as np
try:
    from .route import get_coordinates, get_attraction_coordinates, Route
    from .customer import Customer
    from .attraction import Attraction
    from .monitor import Monitor
except:
    from route import get_coordinates, get_attraction_coordinates, Route
    from customer import Customer
    from attraction import Attraction
    from monitor import Monitor
import pickle

WIDTH = 36
HEIGHT = 36
RADIUS = int(WIDTH/2)
NUM_OBSTACLES = 0
mid_point = (int(WIDTH/2), int(HEIGHT/2))
PENALTY_PERCENTAGE = 5
STRATEGIES = [0.0, 0.25, 0.5, 0.75, 1.0]

# HARDCODED COORDINATES for cluster theme:
xlist, ylist, positions = [12, 21, 26, 11, 9, 25, 25, 26, 20, 12, 11, 21], [17, 26, 13, 17, 18, 12, 11, 12, 28, 16, 18, 29], [(12, 17), (21, 26), (26, 13), (11, 17), (9, 18), (25, 12), (25, 11), (26, 12), (20, 28), (12, 16), (11, 18), (21, 29)]


class Themepark(Model):
    def __init__(self, N_attr, N_cust, width, height, strategy, theme, max_time, weight):
        self.theme = theme
        self.max_time = max_time
        self.N_attr = N_attr
        self.penalty_per = PENALTY_PERCENTAGE
        self.weight = weight
        self.weight_init = weight
        self.strategies = STRATEGIES
        self.x_list, self.y_list, self.positions = xlist, ylist, positions
        # self.x_list, self.y_list, self.positions = get_attraction_coordinates(WIDTH, HEIGHT, self.N_attr, theme)
        self.happinesses = []
        self.starting_positions = [[int((WIDTH/2)-1), 0], [int(WIDTH/2), 0], [int((WIDTH/2)+1), 0]]
        self.path_coordinates = get_coordinates(WIDTH, HEIGHT, NUM_OBSTACLES, self.N_attr, theme)
        self.N_attr = N_attr    # num of attraction agents
        self.N_cust = N_cust    # num of customer agents
        self.width = width
        self.height = height
        self.total_steps = 0
        self.cust_ids = N_cust
        self.strategy = strategy
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = BaseScheduler(self)
        self.schedule_Attraction = BaseScheduler(self)
        self.schedule_Customer = BaseScheduler(self)
        self.totalTOTAL = 0
        self.attractions = self.make_attractions()
        self.running = True
        self.data = []
        self.data_customers = []
        self.park_score = []
        self.data_dict = {}
        self.hist_random_strat = []
        self.hist_close_strat = []
        self.all_rides_list = []
        self.strategy_composition = self.make_strategy_composition()
        self.memory = 5
        self.customer_score = []
        self.customers = self.add_customers(self.N_cust)

        for attraction in self.get_attractions():
            self.data_dict[attraction.unique_id] = ({
                               "id": attraction.unique_id,
                               "length": attraction.attraction_duration,
                               "waiting_list": []})

        self.datacollector = DataCollector(
            {"0.00": lambda m: self.strategy_counter(self.strategies[0]),
            "0.25": lambda m: self.strategy_counter(self.strategies[1]),
            "0.50": lambda m: self.strategy_counter(self.strategies[2]),
            "0.75": lambda m: self.strategy_counter(self.strategies[3]),
            "1.00": lambda m: self.strategy_counter(self.strategies[4]),
            })

        self.total_waited_time = 0

        self.monitor = Monitor(self.max_time, self.N_attr, self.positions)


    def strategy_counter(self, strategy):
        counter_total = {}

        for attraction_pos in self.positions:

            agents = self.grid.get_neighbors(
                attraction_pos,
                moore=True,
                radius=0,
                include_center=True
            )

            counter = 0
            for agent in self.customers:
                if agent.weight == strategy:
                    counter += 1

        return counter

    def make_strategy_composition(self):
        dict = {self.strategies[0]: 0.20, self.strategies[1]:0.20, self.strategies[2]:0.20,
                        self.strategies[3]:0.20, self.strategies[4]:0.20}

        return dict

    def make_attractions(self):
        """ Initialize attractions on fixed position."""

        attractions = {}
        for i in range(self.N_attr):

            pos = (self.x_list[i], self.y_list[i])
            if self.grid.is_cell_empty(pos):

                name = str(i)
                a = Attraction(i, self, pos, name, self.N_cust, self.weight)
                attractions[i] = a

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

        weights_list = []

        if self.weight_init is None:
            for i in range(round(N_cust*self.strategy_composition[0.0])):
                weights_list.append(0)

            for i in range(round(N_cust*self.strategy_composition[0.25])):
                weights_list.append(0.25)

            for i in range(round(N_cust*self.strategy_composition[0.5])):
                weights_list.append(0.5)

            for i in range(round(N_cust*self.strategy_composition[0.75])):
                weights_list.append(0.75)

            for i in range(round(N_cust*self.strategy_composition[1.0])):
                weights_list.append(1.0)
        else:
            for i in range(round(N_cust)):
                weights_list.append(self.weight)

        cust_list = []
        for i in range(N_cust):

            # pos_temp = random.choice(self.starting_positions)
            pos_temp = [random.randint(0,WIDTH-1),random.randint(0,HEIGHT-1)]
            rand_x, rand_y = pos_temp[0], pos_temp[1]

            pos = (rand_x, rand_y)

            # print("Creating CUSTOMER agent {2} at ({0}, {1})"
            #       .format(rand_x, rand_y, i))
            if added is True:
                i = self.cust_ids

            a = Customer(i, self, pos, self.x_list, self.y_list, self.positions, self.strategy, self.weight)
            self.schedule_Customer.add(a)
            a.weight = weights_list[i]

            self.grid.place_agent(a, pos)
            cust_list.append(a)

        return cust_list

    def calculate_people(self):
        """Calculate how many customers are in which attraction."""

        counter_total = {}

        for attraction_pos in self.positions:

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

        return list(counter_total.values())

    def calc_waiting_time(self):

        counter_total = {}

        attractions = self.get_attractions()
        for attraction in attractions:

            counter_total[attraction.unique_id] = attraction.current_waitingtime

        return counter_total


    def calculate_people_sorted(self):
        """
        Calculate how many customers are in which attraction.
        Returns a SORTED LIST.
        For example: indexes = [3, 2, 5, 1, 4]
        indicates that attraction3 has the least people waiting.
        """

        counter_total = {}

        for attraction_pos in self.positions:

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
        return counter_total

    def make_route(self):
        """Draw coordinates of a possible path."""

        for i in range(len(self.path_coordinates)):
            pos = self.path_coordinates[i]

            if pos not in self.positions:

                # Create path agent
                path = Route(i, self, pos)
                self.schedule.add(path)

                self.grid.place_agent(path, pos)

    def get_themepark_score(self):
        """
        Get score of a themepark based on:
            - A total of all waitingtimes for every customer
            - TODO
        """
        attractions = self.get_attractions()
        total_wait, total_rides = 0, 0
        for attraction in attractions:
            total_wait += attraction.current_waitingtime

            if attraction.current_a is not None:
                total_rides += 1

        if total_rides == 0:
            return total_rides

        return (total_wait / total_rides)

    def get_strategy_history(self):
        """ Update history with how many customers chose which strategy """

        customers = self.get_customers()
        randomstrat, closebystrat = 0, 0

        for customer in customers:
            if customer.strategy == "Random":
                randomstrat += 1
            elif customer.strategy == "Closest_by":
                closebystrat += 1

        self.hist_random_strat.append(randomstrat)
        self.hist_close_strat.append(closebystrat)

    def get_customers(self):
        agents = self.grid.get_neighbors(
            mid_point,
            moore=True,
            radius=RADIUS,
            include_center=True)

        customers = []

        # Count customer agents
        for agent in agents:
            if type(agent) == Customer:
                customers.append(agent)
        return customers

    def get_data_customers(self):
        """ Return dictionary with data of customers """

        data = {}
        agents = self.grid.get_neighbors(
            mid_point,
            moore=True,
            radius=RADIUS,
            include_center=True)

        for agent in agents:
            if type(agent) is Customer:
                data[agent.unique_id] = {
                "totalwaited": agent.total_ever_waited,
                "visited_attractions": agent.nmbr_attractions,
                "strategy": agent.strategy
                }
        return data

    def calc_hapiness(self):
        """
        Calculate mean hapiness of all customers, based on:

        - How many rides were taken
        - Number of times in the same attraction
        - Total waiting time
        """
        customers = self.get_customers()

        scores = []

        for customer in customers:
            history = customer.history
            values = list(history.values())
            total_rides = sum(values)

            if total_rides != 0:
                scores.append(total_rides / self.N_attr - self.totalTOTAL / customer.total_ever_waited)
            else:
                return None

        scores = np.interp(scores, (min(scores), max(scores)), (1, 10))
        return np.mean(scores)

    def get_history_list(self):

        customers = self.get_customers()

        histories = {}

        for customer in customers:
            history = customer.history
            values = list(history.values())
            histories[customer.unique_id] = values
        return histories

    def final(self):
        """ Return data """

        cust_data = self.get_data_customers()
        histories = self.get_history_list()

        pickle.dump(self.datacollector.get_model_vars_dataframe(), open("../data/stategy_history.p", 'wb'))
        pickle.dump(cust_data, open("../data/customers.p", 'wb'))
        pickle.dump(self.park_score[-1], open("../data/park_score.p", "wb"))
        pickle.dump(self.happinesses, open("../data/hapiness.p", "wb"))
        pickle.dump(histories, open("../data/cust_history.p", 'wb'))

        print()
        print("RUN HAS ENDED")
        print()
        # quit()

    def save_data(self):
        """Save data of all attractions and customers."""

        # Get info
        waitinglines = self.calc_waiting_time()

        for i in range(len(self.attractions)):
            self.data_dict[i]["waiting_list"].append(waitinglines.get(i))

        self.park_score.append(sum(waitinglines.values()))
        self.happinesses.append(self.calc_hapiness())

    def step(self):
        """Advance the model by one step."""

        if self.totalTOTAL < self.max_time:
            self.totalTOTAL += 1
            self.schedule.step()
            self.datacollector.collect(self)

            self.schedule_Customer.step()
            self.schedule_Attraction.step()

            # update memory of attractions
            # attractions = self.get_attractions()
            # for attraction in attractions:
            #     attraction.update_memory()

            self.total_steps += 1

            self.save_data()
            self.get_strategy_history()

        else:
            self.final()
