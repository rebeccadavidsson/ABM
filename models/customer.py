from mesa import Agent
import random
import math
try:
    from .route import Route
except:
    from route import Route
import numpy as np
import math
# from model import calculate_people

WIDTH = 36
HEIGHT = 36
MEMORY = 5
starting_positions = [(int((WIDTH/2)-1), 0), (int(WIDTH/2), 0), (int((WIDTH/2)+1), 0)]


class Customer(Agent):
    def __init__(self, unique_id, model, pos, x_list, y_list, positions, strategy, weight, adaptive):
        super().__init__(unique_id, model)
        self.pos = pos
        self.model = model
        self.unique_id = unique_id

        self.x_list = x_list
        self.y_list = y_list
        self.positions = positions
        self.current_a = None
        self.strategy = strategy
        self.history = self.make_history()
        self.weight = weight
        if weight == "Random_test_4":
            self.strategy = "Random_test_4"
        self.adaptive = adaptive
        self.all_strategies =  [x for x in self.model.strategies if x != 'Random_test_4']
        if self.strategy == 'Random' or self.strategy == "Random_test_4":
            self.destination = random.choice(positions)
            while self.destination is self.pos:
                self.destination = random.choice(positions)

        if self.strategy == 'Closest_by':

            self.destination = self.closest_by().pos


        self.changed_strategy = False
        self.waitingtime = None
        self.waiting = False
        self.total_ever_waited = 0
        self.nmbr_attractions = 0
        self.waited_period = 0
        self.sadness_score = 0
        self.in_attraction = False
        self.in_attraction_list = []
        self.strategy = strategy
        self.goals = self.get_goals()
        self.memory_strategy = MEMORY
        self.memory_succeses = []
        self.changes_memory = []
        self.strategy_choice = [0,0,0,0,0]

        self.prediction_strategies = self.prediction_all_strategies()
        self.strategy_swap_hist = 0
        # self.several_weights = [0,0.25, 0.5, 0.75, 1]


    def get_goals(self):
        """Set random goals."""
        goals = []
        attractions = self.model.get_attractions()
        for attr in attractions:
            goals.append(attr)
        return goals

    def make_history(self):
        history = {}
        attractions = self.model.attractions
        for attraction in range(len(attractions)):
            history[attractions[attraction]] = 0

        return history

    def penalty(self, current_attraction):
        """
        This method calculates a penalty for attractions that were visited more
        often than other attractions
        """

        total_difference_sum = 0
        if current_attraction == 0:
            return 0
        for i in range(len(self.model.attractions.values())):
            attraction = self.model.attractions[i]

            difference = self.history[current_attraction] - self.history[attraction]

            total_difference_sum += difference

        if total_difference_sum < 0:
            total_difference_sum = 0

        penalty = total_difference_sum * self.model.penalty_per

        return penalty

    def move(self):
        '''
        This method should get the neighbouring cells (Moore's neighbourhood),
        select one, and move the agent to this cell.
        '''

        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            radius=1,
            include_center=False
        )
        obstacles_check = self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=False,
            radius=1
        )

        for obj in obstacles_check:
            if type(obj) is Route:
                try:
                    possible_steps.remove(obj.pos)
                except ValueError:
                    continue # TODO, voor als we obstakels willen

        # start with random choice of position
        temp = random.choice(possible_steps)

        # Loop over every possible step to get fastest step
        for step in possible_steps:

            # check if step is closer to destination
            if (abs(step[0] - self.destination[0]) < abs(temp[0] - self.destination[0]) or
               abs(step[1] - self.destination[1]) < abs(temp[1] - self.destination[1])):
               temp = step

        new_position = temp

        if new_position == self.destination and self.waiting is False:
            self.model.grid.move_agent(self, new_position)

            # Get object of current attraction
            attractions = self.model.get_attractions()
            for attraction in attractions:
                if attraction.pos == new_position:
                    current_a = attraction
            self.current_a = current_a

            self.set_waiting_time()
            self.waiting = True

        # Extra check to see if agent is at destination
        if self.check_move() is True:
            self.model.grid.move_agent(self, new_position)

    def check_move(self):
        """ Checks if a move can be done, given a new position."""

        if self.waitingtime is not None:

            # set in ride to true false
            if self.current_a is not None:
                if self.waited_period == self.waitingtime - self.current_a.attraction_duration:
                    self.in_attraction = True

            # CHANGE DIRECTION if waitingtime is met
            if self.waitingtime <= self.waited_period:

                # when attraction is left set self.attraction to false
                self.in_attraction = False

                # Update goals and attraction
                for attraction in self.model.get_attractions():
                    if attraction.pos == self.pos:
                        if attraction.N_current_cust > 0:
                            attraction.N_current_cust -= 1
                            self.model.attraction_history[attraction][self.model.totalTOTAL] -=1

            if self.waitingtime == self.waited_period:

                if self.current_a is not None:
                    self.history[self.current_a] += 1

                    # Only update when adaptive strategy is on
                    if self.adaptive is True:
                        if self.strategy is not "Random":
                            if self.strategy is not "Random_test_4":
                                self.update_strategy()

                # increment number of rides taken of attraction
                # if self.current_a is not None:
                self.current_a.rides_taken += 1

                # increment number of rides taken of customer
                self.nmbr_attractions += 1
                self.total_ever_waited += self.waited_period
                self.waited_period = 0

                # Update memory
                # if self.init_weight is None:
                #     self.update_strategy()

                # Set current attraction back to None when customer leaves.
                self.current_a = None

                if self.strategy == "Closest_by":
                    self.destination = self.closest_by().pos
                elif self.strategy == 'Random' or self.strategy == "Random_test_4":
                    self.destination = random.choice(self.positions)
                    while self.destination is self.pos:
                        self.destination = random.choice(self.positions)
                self.waiting = False
                self.waited_period = 0

        if self.pos == self.destination:

            # if self.waited_period == 0:
                # if self.init_weight is None:

            # Check which attraction
            attractions = self.model.get_attractions()
            for attraction in attractions:
                if attraction.pos == self.pos:
                    self.current_a = attraction

            # self.current_a. += 1
            self.waited_period += 1

        if self.waiting is False:
            return True
        return False

    def set_waiting_time(self):
        '''
        This method calculates the waiting time of the customer based on the
        number of customers in line, and the duration of the attraction
        '''
        attractions = self.model.get_attractions()
        attraction = None
        for i in attractions:
            if self.pos == i.pos:
                attraction = i
                break

        # Update waitingtime of attraction
        attraction.N_current_cust += 1

        self.model.attraction_history[attraction][self.model.totalTOTAL] +=1
        attraction.calculate_waiting_time()

        # add waiting time to agent
        self.waitingtime = attraction.current_waitingtime

    def get_walking_distances(self):
        """
        Return index of attraction-id with shortest walking distance.
        Function uses pythagoras formula.
        For example:
        indexes = [3, 2, 5, 1, 4]
        indicates that attraction3 has the shortest walking distance.
        """
        attractions = self.model.get_attractions()

        distances = {}
        for attraction in attractions:

            # Stelling van pythagoras
            p1, p2 = self.pos, attraction.pos
            dist = math.sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))
            distances[attraction.unique_id] = dist

        # Sort by shortest distance
        indexes = []
        {indexes.append(k): v for k, v in sorted(distances.items(), key=lambda item: item[1])}

        return distances

    def get_waiting_lines(self):
        """
        Return index of attraction-id with shortest waiting lines.
        For example:
        indexes = [3, 2, 5, 1, 4]
        indicates that attraction3 has the shortest waiting line.
        """
        people = self.model.calculate_people_sorted()
        return people

    def get_score(self, distances, waitinglines):
        """
        Return a score of distance + watingtime for all attractions.
        """

        scores = {}

        for i in range(len(distances)):
            scores[i] = distances.get(i) + waitinglines.get(i)

        return scores

    def update_strategy2(self):
        """
        Update an agents memory and change strategy based on memory.
        """
        counter = 0

        # If all past steps weren't succesful, change strategy
        if len(self.memory_succeses) >= self.memory_strategy:
            for num in self.memory_succeses:
                if num == 0:
                    counter += 1

            # Change strategy
            if counter == self.memory_strategy and self.changed_strategy is False:
                # ___________________________________________________
                # COMMMENTEN als je niet strategie wilt veranderen
                # if self.strategy == "Random":
                #     self.strategy = "Closest_by"
                # else:
                #     self.strategy = "Random"

                self.changed_strategy = True
                self.memory_succeses.append(1)
                self.memory_succeses.pop()
        else:

            # Determine if strategy was succesful.
            # Take into account: waitingtimes of all other attractions.
            # TODO: nog iets anders?
            waitinglines = self.get_waiting_lines()

            # if succes:
            succes = []
            for value, key in waitinglines.items():
                if key == min(waitinglines.keys()):
                    succes.append(value)

            if waitinglines.get(self.current_a.unique_id) in succes:
                self.memory_succeses.append(1)

            # No succes
            else:
                self.memory_succeses.append(0)

    def update_strategy3(self):

            strategy_ranking = {}
            queues = self.get_waiting_lines()
            chosen_strategy = self.weight

            if self.current_a is not None:
                # for attraction in queues.keys():
                #     if queues[attraction] < queues[self.current_a.unique_id]:
                #         print("VERKEERDE STRATEGY, attraction:", attraction, "nr:", self.unique_id)
                for strategy in self.prediction_strategies.keys():
                    attraction = self.prediction_strategies[strategy][0]
                    if queues[attraction.unique_id] < queues[self.current_a.unique_id] and not strategy == chosen_strategy:

                        # strategy_ranking[strategy] = queues[attraction.unique_id] + self.prediction_strategies[strategy][1]
                        strategy_ranking[strategy] = queues[attraction.unique_id]

                if len(strategy_ranking.values()) > 0:
                    minval = min(strategy_ranking.values())
                    res = [k for k, v in strategy_ranking.items() if v == minval]
                    if len(res) is 1:
                        best_strat = res[0]
                    else:
                        best_strat = random.choice(res)
                    self.weight = best_strat

    def update_strategy(self):

        strategy_ranking = {}
        queues = self.get_waiting_lines()
        chosen_strategy = self.weight
        current_walking_distance = self.prediction_strategies[chosen_strategy][1]
        current_arrival_time = math.ceil(self.prediction_strategies[chosen_strategy][2])
        # print("chosen_strategy:", chosen_strategy, ",line:",
        #         self.model.attraction_history[self.current_a][current_arrival_time],
        #         "curr_time:", self.model.totalTOTAL, ",ID", self.unique_id, ",arrivaltime",
        #         current_arrival_time)
        if self.current_a is not None:

            for strategy in self.prediction_strategies.keys():
                if strategy == chosen_strategy:
                    continue

                attraction = self.prediction_strategies[strategy][0]
                arrival_time = math.ceil(self.prediction_strategies[strategy][2])
                walking_distance = self.prediction_strategies[strategy][1]

                if attraction == self.current_a:
                    continue

                if math.ceil(arrival_time) < self.model.totalTOTAL:

                    queue_at_arrival = self.model.attraction_history[attraction][math.ceil(arrival_time)]
                    if arrival_time + queue_at_arrival + attraction.attraction_duration < self.model.totalTOTAL:
                        # print("strategy:", strategy, ",arrival_time:", arrival_time, ",attraction", attraction.unique_id)
                        #
                        # print("time after going on ride:", arrival_time + queue_at_arrival + attraction.attraction_duration)


                        strategy_ranking[strategy] = arrival_time + queue_at_arrival


            if len(strategy_ranking.values()) > 0:
                minval = min(strategy_ranking.values())
                res = [k for k, v in strategy_ranking.items() if v == minval]
                if len(res) is 1:
                    best_strat = res[0]
                else:
                    best_strat = random.choice(res)
                self.weight = best_strat
                self.strategy_swap_hist += 1



    def step(self):
        """
        This method should move the customer using the `random_move()` method.
        """

        if self.waiting is True:
            self.sadness_score += 1

        if self.in_attraction is True:
            self.in_attraction_list.append(1)
        else:
            self.in_attraction_list.append(0)

        self.move()

    def closest_by(self):
        """
        This method returns the attraction closest by the customer
        Adds a deterministic penalty per attraction based on the penalty method.
        """
        predictions = self.get_walking_distances()

        # add waitingtimes
        waiting_times = self.get_waiting_lines()

        # print(self.weight)

        for i in range(len(predictions.keys())):

            if self.weight is "random":
                predictions[i] = predictions[i] + waiting_times[i]
            else:
                predictions[i] = predictions[i] * (1 - self.weight) + waiting_times[i] * self.weight


        maxval = max(predictions.values())
        for attraction_nr in predictions:
            penalty = self.penalty(self.model.attractions[attraction_nr])

            predictions[attraction_nr] = predictions[attraction_nr] + maxval * (penalty/100)

        minval = min(predictions.values())
        res = [k for k, v in predictions.items() if v == minval]
        if len(res) is 1:
            predicted_attraction = res[0]
        else:
            predicted_attraction = random.choice(res)
        attraction_object = self.model.get_attractions()[predicted_attraction]
        # dit kan volgens mij ook:
        # attraction_object = self.attractions[predicted_attraction]
        self.prediction_strategies = self.prediction_all_strategies()

        return self.model.attractions[predicted_attraction]


    def prediction_all_strategies(self):

        prediction_per_strategy = {}

        predictions = self.get_walking_distances()


        # add waitingtimes
        waiting_times = self.get_waiting_lines()
        # print(len(predictions.keys()))
        # print(predictions, waiting_times, "PRINT")

        for weight in self.all_strategies:
            for i in range(len(predictions.keys())):

                if self.weight is None:
                    predictions[i] = predictions[i] + waiting_times[i]
                else:
                    predictions[i] = predictions[i] * (1 - weight) + waiting_times[i] * weight


            maxval = max(predictions.values())
            for attraction_nr in predictions:
                penalty = self.penalty(self.model.attractions[attraction_nr])

                predictions[attraction_nr] = predictions[attraction_nr] + maxval * (penalty/100)

            minval = min(predictions.values())
            res = [k for k, v in predictions.items() if v == minval]
            if len(res) is 1:
                predicted_attraction = res[0]
            else:
                predicted_attraction = random.choice(res)
            attraction_object = self.model.get_attractions()[predicted_attraction]
            # dit kan volgens mij ook:
            # attraction_object = self.attractions[predicted_attraction]
            predictions = self.get_walking_distances()
            arrival_time = self.model.totalTOTAL + predictions[predicted_attraction]
            prediction_per_strategy[weight] = [self.model.attractions[predicted_attraction], predictions[predicted_attraction],
                                                arrival_time]
        return prediction_per_strategy
