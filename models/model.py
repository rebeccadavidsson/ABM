from mesa import Model
from mesa.space import MultiGrid
from mesa.time import BaseScheduler
from mesa.datacollection import DataCollector
import random
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


class Themepark(Model):
    def __init__(self, N_attr, N_cust, width, height, strategy, theme, max_time, memory):
        self.theme = theme
        self.max_time = max_time
        self.N_attr = N_attr
        self.penalty_per = PENALTY_PERCENTAGE
        self.memory = memory
        self.x_list, self.y_list, self.positions = get_attraction_coordinates(WIDTH, HEIGHT, self.N_attr, theme)
        self.starting_positions = [[int((WIDTH/2)-1), 0], [int(WIDTH/2), 0], [int((WIDTH/2)+1), 0]]
        self.path_coordinates = get_coordinates(WIDTH, HEIGHT, NUM_OBSTACLES, self.N_attr, theme)
        self.N_attr = N_attr    # num of attraction agents
        self.N_cust = N_cust    # num of customer agents
        self.waiting_times = [5.0] * self.N_attr
        self.customer_capacity = [5.0] * self.N_attr
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
        self.add_customers(self.N_cust)

        for attraction in self.get_attractions():
            self.data_dict[attraction.unique_id] = ({
                               "id": attraction.unique_id,
                               "length": attraction.attraction_duration,
                               "waiting_list": []})

        # Dynamic datacollector (werkt niet :( )
        # self.datacollector = DataCollector(self.datacollection_dict())

        # Hardcoded datacollector
        self.datacollector = DataCollector(
            {"Attraction1": lambda m: self.schedule_Attraction.agents[0].customers_inside(),
            "Attraction2": lambda m: self.schedule_Attraction.agents[1].customers_inside(),
            "Attraction3": lambda m: self.schedule_Attraction.agents[2].customers_inside(),
            "Attraction4": lambda m: self.schedule_Attraction.agents[3].customers_inside(),
            "Attraction5": lambda m: self.schedule_Attraction.agents[4].customers_inside(),
            "Attraction6": lambda m: self.schedule_Attraction.agents[5].customers_inside(),
            "Attraction7": lambda m: self.schedule_Attraction.agents[6].customers_inside()
            })

        self.total_waited_time = 0

        self.monitor = Monitor(self.max_time, self.N_attr, self.positions)

    # def datacollection_dict(self):
    #     """ Returns a dictionary for the DataCollector. """
    #
    #     dict = {}
    #     for i in range(self.N_attr):
    #         dict["Attraction{}".format(i)] = lambda m: self.schedule_Attraction.agents[i].customers_inside()
    #
    #     return dict


    def make_attractions(self):
        """ Initialize attractions on fixed position."""

        attractions = {}
        for i in range(self.N_attr):

            pos = (self.x_list[i], self.y_list[i])
            if self.grid.is_cell_empty(pos):
                # print("Creating ATTRACTION agent {2} at ({0}, {1})"
                #       .format(x_list[i], y_list[i], i))

                # TODO vet leuke namen verzinnen voor de attracties
                name = str(i)
                a = Attraction(i, self, self.waiting_times[i], self.customer_capacity[i], pos, name, self.N_cust, self.memory)
                attractions[i] = a
                # print(a.waiting_time, "waitingtime")
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

            # pos_temp = random.choice(self.starting_positions)
            pos_temp = [random.randint(0,WIDTH-1),random.randint(0,HEIGHT-1)]
            rand_x, rand_y = pos_temp[0], pos_temp[1]

            pos = (rand_x, rand_y)

            # print("Creating CUSTOMER agent {2} at ({0}, {1})"
            #       .format(rand_x, rand_y, i))
            if added is True:
                i = self.cust_ids

            # self.strategy = random.choice(["Random", "Closest_by"])
            a = Customer(i, self, pos, self.x_list, self.y_list, self.positions, self.strategy, self.memory)
            self.schedule_Customer.add(a)

            self.grid.place_agent(a, pos)

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

    def get_durations(self):
        """ Get duratiosn of every attraction in a list """

        durations = []

        for attraction_pos in self.positions:

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

        for i in range(len(self.path_coordinates)):
            pos = self.path_coordinates[i]

            if pos not in self.positions:

                # Create path agent
                path = Route(i, self, pos)
                self.schedule.add(path)

                self.grid.place_agent(path, pos)

    def get_themepark_score(self):
        """
        Get current waiting time of the themepark
        """
        attractions = self.get_attractions()
        total_current = 0
        for attraction in attractions:
            total_current += attraction.current_waitingtime

        return total_current


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


    def final(self):
        """ Return data """

        cust_data = self.get_data_customers()

        # pickle.dump(self.data_dict, open("../data/attractions2.p", 'wb'))
        # pickle.dump(cust_data, open("../data/customers2.p", 'wb'))
        # pickle.dump(self.park_score, open("../data/park_score.p", "wb"))

        pickle.dump(self.data_dict, open("../data/attractions2.p", 'wb'))
        pickle.dump(cust_data, open("../data/customers2.p", 'wb'))
        pickle.dump(self.park_score, open("../data/park_score_mem{}.p".format(self.memory), "wb"))
        pickle.dump(self.hist_random_strat, open("../data/strategy_random.p", "wb"))
        pickle.dump(self.hist_close_strat, open("../data/strategy_close.p", "wb"))

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



    def step(self):
        """Advance the model by one step."""

        if self.totalTOTAL < self.max_time:
            self.totalTOTAL += 1
            self.schedule.step()
            self.datacollector.collect(self)

            self.schedule_Customer.step()
            self.schedule_Attraction.step()

            # update memory of attractions
            attractions = self.get_attractions()
            for attraction in attractions:
                attraction.update_memory()

            self.total_steps += 1

            self.save_data()
            self.get_strategy_history()

        else:
            self.final()
