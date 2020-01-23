from mesa import Agent
import random
import math
import numpy as np
from .route import get_coordinates, Route
from .attraction import Attraction
from scipy.spatial import distance
import heapq
# from model import calculate_people

WIDTH = 36
HEIGHT = 36
NUM_OBSTACLES = 20
starting_positions = [(int((WIDTH/2)-1), 0), (int(WIDTH/2), 0), (int((WIDTH/2)+1), 0)]


class Customer(Agent):
    def __init__(self, unique_id, model, pos, x_list, y_list, positions, strategy):
        super().__init__(unique_id, model)
        self.pos = pos
        self.model = model
        self.unique_id = unique_id
        self.x_list = x_list
        self.y_list = y_list
        self.positions = positions

        self.destination = random.choice(positions)
        while self.destination is self.pos:
            self.destination = random.choice(positions)

        self.waitingtime = None
        self.waiting = False
        self.total_ever_waited = 0

        # Start waited period with zero
        self.waited_period = 0
        self.current_a = None
        self.sadness_score = 0
        self.in_attraction = False


        self.strategy = strategy
        if self.strategy == "Random":
            self.has_app = False
        elif self.strategy == "Knowledge":
            self.has_app = False

        else:
            raise Exception('\033[93m' + "This method is not implemented!!!" + '\033[0m')
            quit()

        self.guided = False

        # Random if customer has the app
        self.goals = self.get_goals()
        self.reached_goals = False

        self.leaving = False

        if self.has_app is True:
            self.checked_app = False
            self.destination = self.search_best_option()

        self.memory_strategy = 1


    def get_goals(self):
        """Set random goals."""

        attractions = self.model.get_attractions()
        r = random.randint(1, len(attractions))
        goals = []
        for i in range(r):
            rand_choice = random.choice(attractions)
            goals.append(rand_choice)
            attractions.remove(rand_choice)
        # goals.append(attractions[3])
        # goals.append(attractions[4])
        # goals.append(attractions[5])

        return goals

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

            if self.leaving is True:
                self.model.schedule_Customer.remove(self)
                # self.model.grid[self.pos[0]][self.pos[1]] = None
                # TODO: stip ook verwijderen
            else:

                # Only move if there is no queue
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

        if self.pos == self.destination:

            # Check which attraction
            attractions = self.model.get_attractions()
            for attraction in attractions:
                if attraction.pos == self.pos:
                    self.current_a = attraction

            # self.current_a. += 1
            self.waited_period += 1

        # CHANGE DIRECTION if waitingtime is met
        if self.waitingtime is not None:

            if self.waitingtime <= self.waited_period:

                # # reset ride time
                # if self.current_a is not None:
                #     attraction = self.current_a
                #     attraction.ride_time = 0

                # Update goals and attraction
                for attraction in self.goals:

                    if attraction.pos == self.pos:

                        # set checked_app = False so app can be checked at the
                        # first step when cstomer walks away from an attraction.
                        self.checked_app = False
                        self.goals.remove(attraction)
                        self.sadness_score -= 20
                        if attraction.N_current_cust > 0:
                            attraction.N_current_cust -= 1
                        # attraction.calculate_waiting_time()

                    break

                # Check if agent needs to leave or go to new goal
                if len(self.goals) > 0:
                    self.get_destination()
                elif self.leaving is False:
                    self.leaving = True
                    self.destination = random.choice(starting_positions)
                    self.waiting = False

            if self.waitingtime == self.waited_period:

                self.current_a = None

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

        self.waitingtime = attraction.current_waitingtime

        # Update waitingtime of attraction
        attraction.N_current_cust += 1
        attraction.calculate_waiting_time()

        # # get number of customers in line
        waiting_lines = self.model.calculate_people()

        # get attraction durations
        durations = self.model.get_durations()

        # get current attraction from destination
        index = self.positions.index(self.destination)

        # calculate waitingtime
        waitingtime = durations[index] * waiting_lines[index]

        # add waiting time to agent
        self.waitingtime = waitingtime

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

    def helpers_best_choice(self, distances, waitinglines, index):
        """
        Helpers function for search_best_option().
        Returns an index of the best choice.
        """

        scores = self.get_score(distances, waitinglines)

        # Start with best solution
        temp = scores.get(index)

        for i in range(index, len(scores) + 1):

            if not scores.get(i + 1):
                return i
            if scores.get(i + 1) < scores.get(i):
                return i + 1
            else:
                return i
    def strategy_distance():
        pass

    def strategy_time():
        pass




    def search_best_option(self):
        """
        Get best choice of attraction based on watingtime and distance.
        Returns a position of the best attraction.
        Start with best solution; shortest distance and shortest waiting line,
        if this solution is not in list of goals, go to second best solution.
        So: ONLY includes attractions in personal GOALS LIST.
        """

        distances = self.get_walking_distances()
        waitinglines = self.get_waiting_lines()

        goals_positions = []
        [goals_positions.append(goal.pos) for goal in self.goals]

        # Start with best solution and check if this solution is in goals
        index = 0

        best_choice = self.helpers_best_choice(distances, waitinglines, index)

        # Empty goals list, TODO
        if goals_positions == []:
            return None

        while self.positions[best_choice] not in goals_positions and index < len(self.positions):
            best_choice = self.helpers_best_choice(distances, waitinglines, index)
            index += 1

        # Best choice is found!!!
        return self.positions[best_choice]

    def get_shortest_dest(self):
        """
        Get destination from list of goals
        with SHORTEST WATINGTIME for people with the app.
        Not based on walking distance.
        """

        if len(self.goals) == 1:
            self.destination = self.goals[0].pos
            self.goals = []

            return None, None
        else:
            destinations, waiting_lines = [], []
            [destinations.append(attraction) for attraction in self.goals]

            # Get minimum watingtime
            waiting_lines = []
            [waiting_lines.append(dest.current_waitingtime) for dest in destinations]

            minimum = min(waiting_lines)

            return destinations[waiting_lines.index(minimum)].pos, waiting_lines

    def get_destination(self):
        '''
        Gives the agent a new destination based on goal and waiting time.
        '''
        dest, waiting_lines = self.get_shortest_dest()

        if dest is not None:

            # Change current destination to new destination
            self.destination = dest

        # If new destination is current attraction choose second closest
        if self.pos == self.destination:

            if self.has_app is True:
                second_shortest = sorted(waiting_lines)[1]
            else:
                # TODO: Ik weet niet of dit nou helemaal goed gaat, even checken
                # of dit mag met gewoon random eentje kiezen als die persoon
                # de app niet heeft en dus niet weet wat de kortste wachtrij is.
                second_shortest = random.choice(waiting_lines)
            # check if two waiting times are of same length
            indexi = []
            for i in range(len(waiting_lines)):
                if waiting_lines[i] == second_shortest:
                    indexi.append(i)
            if len(indexi) > 1:
                # TODO: volgens mij kan deze hele for-loop weg...
                for i in indexi:
                    if self.positions[i] != self.pos:
                        self.destination = self.positions[i]
                        break
            else:
                self.destination = self.positions[waiting_lines.index(second_shortest)]

        self.waiting = False
        self.waited_period = 0
        return False

    def update_choice(self):
        """
        Update customers choice of destination at every move, mainly for people
        who have the app.
        Destination choice can change based on knowledge about waitingtimes.
        """

        # Check again for best option
        best = self.search_best_option()
        print(best, "best")
        if best is not None:
            self.destination = best


        if self.guided is True and best is not None:
            self.destination = self.model.monitor.make_prediction(self.model.totalTOTAL,self.goals, self.get_walking_distances(),)

    def step(self):
        """
        This method should move the customer using the `random_move()` method.
        """

        # Update customer choice of destination while walking,
        # only for those who have the app


        if self.has_app is True and self.checked_app is False:
            print("hoi")
            self.update_choice()
            self.checked_app = True

        if self.waiting is True:
            self.sadness_score += 1

        self.move()

        # TODO: Voor elke stap de wachttijd laten afnemen
        # if self.current_a:
        #     print(self.current_a.unique_id)

    def closest_by():
        Predictions = {}
        minval = min(predictions.values())
        res = [k for k, v in predictions.items() if v==minval]
        if len(res) is 1:
            predicted_attraction = res[0]
        else:
            predicted_attraction = random.choice(res)
        return predicted_attraction
