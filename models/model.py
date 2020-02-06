from mesa import Model
from mesa.space import MultiGrid
from mesa.time import BaseScheduler
from mesa.datacollection import DataCollector
import random
import numpy as np
import pickle
import matplotlib.pyplot as plt
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


FRACTION_RANDOM = 1/6
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
    def __init__(self, N_attr, N_cust, width, height, strategy, theme, max_time, weight, adaptive):
        self.max_time = max_time
        self.N_attr = N_attr
        self.penalty_per = PENALTY_PERCENTAGE
        self.weight = weight
        self.adaptive = adaptive
        self.strategies = STRATEGIES
        self.x_list, self.y_list, self.positions = xlist, ylist, positions
        self.x_list, self.y_list, self.positions = get_attraction_coordinates(WIDTH, HEIGHT, self.N_attr, theme)
        self.happinesses = []
        self.path_coordinates = get_coordinates(WIDTH, HEIGHT, NUM_OBSTACLES, self.N_attr, theme)
        self.N_cust = N_cust    # num of customer agents
        self.total_steps = 0
        self.cust_ids = N_cust
        self.strategy = strategy
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = BaseScheduler(self)
        self.schedule_Attraction = BaseScheduler(self)
        self.schedule_Customer = BaseScheduler(self)
        self.totalTOTAL = 0 #TODO: DEZE NAAM VERANDEREN
        self.attractions = self.make_attractions()
        self.attraction_history = self.make_attr_hist()
        self.park_score = []
        self.data_dict = {}
        self.hist_random_strat = []
        self.hist_close_strat = []
        self.all_rides_list = []
        self.strategy_composition = self.make_strategy_composition()
        self.customers = self.add_customers(self.N_cust)
        self.monitor = Monitor(self.max_time, self.N_attr, self.positions)
        self.running = True



        # TODO: ALS HET GOED IS KUNNEN AL DEZE INITS WEG, MAAR DIT MOETEN WE WEL NOG EVEN DUBBEL CHECKEN
        # --> dit is gecheckt op het runnen van main_cluster_random_noise
        # self.theme = theme
        # self.starting_positions = [[int((WIDTH/2)-1), 0], [int(WIDTH/2), 0], [int((WIDTH/2)+1), 0]]
        # self.width = width
        # self.height = height
        # self.data = []
        # self.data_customers = []
        # self.memory = 5
        # self.customer_score = []
        # self.only_random = False
        # self.total_waited_time = 0

        # Initialize dictionary of attractions
        for attraction in self.get_attractions():
            self.data_dict[attraction.unique_id] = ({
                               "id": attraction.unique_id,
                               "length": attraction.attraction_duration,
                               "waiting_list": []})

        # TODO ADD COMMENT (SNAP NIET WAT DE DATACOLLECTOR IS)
        if len(self.strategies) == 6:
            self.datacollector = DataCollector(

                {"Random": lambda m: self.strategy_counter(self.strategies[0]),
                "0.00": lambda m: self.strategy_counter(self.strategies[1]),
                "0.25": lambda m: self.strategy_counter(self.strategies[2]),
                "0.50": lambda m: self.strategy_counter(self.strategies[3]),
                "0.75": lambda m: self.strategy_counter(self.strategies[4]),
                "1.00": lambda m: self.strategy_counter(self.strategies[5]),
                })
        else:
            self.datacollector = DataCollector(
                {"0.00": lambda m: self.strategy_counter(self.strategies[0]),
                "0.25": lambda m: self.strategy_counter(self.strategies[1]),
                "0.50": lambda m: self.strategy_counter(self.strategies[2]),
                "0.75": lambda m: self.strategy_counter(self.strategies[3]),
                "1.00": lambda m: self.strategy_counter(self.strategies[4]),
                })

        self.datacollector2 = DataCollector(
            {"score": lambda m: self.make_score()})



    def make_score(self):
        """
        Get the efficiency score
        """
        ideal = {}
        cust_in_row = 0
        for i in range(len(self.get_attractions())):
            ideal[i] = self.N_cust/self.N_attr
            cust_in_row += self.get_attractions()[i].N_current_cust

        tot_difference = 0
        for i in range(len(self.get_attractions())):

            difference = abs(cust_in_row/self.N_attr  - self.get_attractions()[i].N_current_cust)
            tot_difference += difference

        fraction_not_right = (tot_difference/self.N_cust)
        return abs(1-(fraction_not_right)) * cust_in_row/self.N_cust

    def make_attr_hist(self):
        """
        Initialize a dictionary in which the history of the attractions can be
        added in.
        """
        attraction_history = {}
        for attraction in self.get_attractions():
            attraction_history[attraction] = [0] * (self.max_time + 1)

        return attraction_history

    def strategy_counter(self, strategy):
        """
        Count how many customers of different strategies are at the attractions
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
            for agent in self.customers:
                if agent.weight == strategy:
                    counter += 1

        return counter

    def make_strategy_composition(self):
        """
        TODO: ANNEMIJN KAN JIJ HIER COMMENTS BIJ DOEN? + RANDOM_TEST_4 WEGHALEN
        """
        if self.strategy == "Random_test_4":
            self.strategies = ["Random_test_4", 0.0, 0.25, 0.50, 0.75, 1.0]
            dict = {self.strategies[0]: 1/6, self.strategies[1]:0.20, self.strategies[2]:0.20,
                            self.strategies[3]:0.20, self.strategies[4]:0.20, self.strategies[5]: 0.20}

            composition_list = []
            for i in range(len(self.strategies)):
                if i == 0:
                    dict[self.strategies[i]] = FRACTION_RANDOM
                    continue
                else:
                    composition_list.append(random.randint(0,100))
            sum_comp = sum(composition_list)

            sum_comp = sum_comp - sum_comp * FRACTION_RANDOM
            for i in range(len(self.strategies)):
                if i == 0:
                    continue
                else:
                    dict[self.strategies[i]] = composition_list[i-1] /sum_comp

        else:
            dict = {self.strategies[0]: 0.20, self.strategies[1]:0.20, self.strategies[2]:0.20,
                            self.strategies[3]:0.20, self.strategies[4]:0.20}

            composition_list = []
            for i in range(len(self.strategies)):

                composition_list.append(random.randint(0,100))

            sum_comp = sum(composition_list)

            sum_comp = sum_comp
            for i in range(len(self.strategies)):

                dict[self.strategies[i]] = composition_list[i-1] /sum_comp

        return dict

    def make_attractions(self):
        """
        Initialize attractions on fixed position.
        """

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
        Get a list with all attractions.
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

    def calculate_people(self):
        """
        Calculate how many customers are in which attraction.
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

        return list(counter_total.values())


    def add_customers(self, N_cust, added=False):
        """
        Initialize customers on random positions.
        """

        weights_list = []
        if self.adaptive is True:

            for j in self.strategy_composition.keys():
                for i in range(round(N_cust*self.strategy_composition[j])):
                    weights_list.append(j)

            if len(weights_list) < self.N_cust:
                rand = random.choice(self.strategies)
                weights_list.append(rand)
            elif len(weights_list) > self.N_cust:
                rand = random.choice(weights_list)
                weights_list.remove(rand)

        else:

            # if the strategy is not random add weights to weights_list
            if self.strategy is not "Random":
                for i in range(round(N_cust)):
                    weights_list.append(self.weight)

        cust_list = []
        for i in range(N_cust):

            pos_temp = [random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)]
            rand_x, rand_y = pos_temp[0], pos_temp[1]

            pos = (rand_x, rand_y)

            if added is True:
                i = self.cust_ids
            if self.strategy == "Random_test_4":
                if weights_list[i] == "Random_test_4":
                    strategy = "Random_test_4"
                else:
                    strategy = "Closest_by"
            else:
                strategy = self.strategy

            # Set weight
            if weights_list == []:
                weight = None
            else:
                weight = weights_list[i]



            # Initialize customer and add customer to the model
            a = Customer(i, self, pos, self.x_list, self.y_list, self.positions, strategy, weight, self.adaptive)
            self.schedule_Customer.add(a)
            self.grid.place_agent(a, pos)
            cust_list.append(a)

        return cust_list

    def calc_waiting_time(self):
        """
        Calculate the waitingtime per attraction
        """

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
            self.attraction_history[attraction][self.totalTOTAL] = counter
            counter_total[attraction.unique_id] = counter

        return counter_total

    def make_route(self):
        """
        Draw coordinates of a possible path.
        """

        for i in range(len(self.path_coordinates)):
            pos = self.path_coordinates[i]

            if pos not in self.positions:

                # Create path agent
                path = Route(i, self, pos)
                self.schedule.add(path)

                self.grid.place_agent(path, pos)


    # TODO: THEMEPARK SCORE GEBRUIKEN WE NIET MEER, DIT ALLEMAAL VERWIJDEREN OVERAL?
    def get_themepark_score(self):
        """
        Get score of a themepark based on:
            - A total of all waitingtimes for every customer
            - The total number of rides taken
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
        """
        Update history with how many customers chose which strategy.
        """

        customers = self.get_customers()
        randomstrat, closebystrat = 0, 0

        for customer in customers:
            if customer.strategy == "Random" or customer.strategy == "Random_test_4":
                randomstrat += 1
            elif customer.strategy == "Closest_by":
                closebystrat += 1

        self.hist_random_strat.append(randomstrat)
        self.hist_close_strat.append(closebystrat)

    def get_customers(self):
        """
        Returns a list of all the customers in the themepark.
        """
        agents = self.grid.get_neighbors(
            mid_point,
            moore=True,
            radius=RADIUS,
            include_center=True)

        customers = []

        # Add customers to list
        for agent in agents:
            if type(agent) == Customer:
                customers.append(agent)

        return customers

    def get_data_customers(self):
        """
        Return dictionary with data of customers.
        """

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
                "strategy": agent.strategy,
                "swapped_strat": agent.strategy_swap_hist
                }

        return data


# TODO: NET ALS THEMEPARK SCORE GEBRUIKEN WE DIT NEIT MEER TOCH????
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
        """
        Create a list with the history of the customers.
        """

        customers = self.get_customers()
        histories = {}

        for customer in customers:
            history = customer.history
            values = list(history.values())
            histories[customer.unique_id] = values
        return histories

    def final(self):
        """
        End run and return data.
        """

        # Create list with at every time step the amount of attractions that are active
        attractions = self.get_attractions()
        self.all_rides_list = [0] * len(attractions[0].in_attraction_list)
        for attraction in attractions:
            for i in range(len(attraction.in_attraction_list)):
                self.all_rides_list[i] += attraction.in_attraction_list[i]

        # Change the all_rides_list into fractions
        for i in range(len(self.all_rides_list)):
            self.all_rides_list[i] /= self.N_attr

        # Initialize history list and get agents
        hist_list = []
        agents = self.grid.get_neighbors(
            mid_point,
            moore=True,
            radius=RADIUS,
            include_center=True)

        # Save history of all customers
        cust_data = self.get_data_customers()
        for agent in agents:
            if type(agent) is Customer:
                sum_attr = sum(agent.history.values())
                if sum_attr > 0:
                    hist_list.append(agent.strategy_swap_hist)
                else:
                    hist_list.append(agent.strategy_swap_hist)

        histories = self.get_history_list()

        # Save data
        try:
            pickle.dump(self.datacollector.get_model_vars_dataframe(), open("../data/strategy_history.p", 'wb'))
            pickle.dump(self.datacollector2.get_model_vars_dataframe(), open("../data/eff_score_history.p", 'wb'))
            pickle.dump(cust_data, open("../data/customers.p", 'wb'))
            pickle.dump(self.park_score[-1], open("../data/park_score.p", "wb"))
            pickle.dump(self.happinesses, open("../data/hapiness.p", "wb"))
            pickle.dump(histories, open("../data/cust_history.p", 'wb'))
        except:
            pickle.dump(self.datacollector.get_model_vars_dataframe(), open("data/strategy_history.p", 'wb'))
            pickle.dump(self.datacollector2.get_model_vars_dataframe(), open("data/eff_score_history.p", 'wb'))
            pickle.dump(cust_data, open("data/customers.p", 'wb'))
            pickle.dump(self.park_score[-1], open("data/park_score.p", "wb"))
            pickle.dump(self.happinesses, open("data/hapiness.p", "wb"))
            pickle.dump(histories, open("data/cust_history.p", 'wb'))

        try:
            pickle.dump(self.all_rides_list, open("../data/all_rides.p", "wb"))
        except:
            pickle.dump(self.all_rides_list, open("data/all_rides.p", "wb"))

        print()
        print("RUN HAS ENDED")
        print()


    def save_data(self):
        """
        Save data of all attractions and customers.
        """
        # Get info
        waitinglines = self.calc_waiting_time()

        for i in range(len(self.attractions)):
            self.data_dict[i]["waiting_list"].append(waitinglines.get(i))

        self.park_score.append(sum(waitinglines.values()))
        self.happinesses.append(self.calc_hapiness())

    def step(self):
        """
        Advance the model by one step.
        """

        # Take a step if max steps is not reached
        if self.totalTOTAL < self.max_time:
            self.totalTOTAL += 1
            self.schedule.step()
            self.datacollector.collect(self)
            self.datacollector2.collect(self)

            self.schedule_Attraction.step()
            self.schedule_Customer.step()

            self.total_steps += 1

            self.save_data()
            self.get_strategy_history()

        # Stop simulation
        else:
            for key in self.attraction_history.keys():
                y = self.attraction_history[key]
                x = list(range(0, self.max_time))

            self.final()
