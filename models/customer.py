from mesa import Agent
import random
import numpy as np
from .route import get_coordinates, Route
from .attraction import Attraction
from scipy.spatial import distance
# from model import calculate_people


# TODO NIEUWE MENSEN IN HET PARK LATEN KOMEN
WIDTH = 36
HEIGHT = 36
NUM_ATTRACTIONS = 5
NUM_OBSTACLES = 20
starting_positions = [(int((WIDTH/2)-1), 0), (int(WIDTH/2), 0), (int((WIDTH/2)+1), 0)]


class Customer(Agent):
    def __init__(self, unique_id, model, pos, x_list, y_list, positions):
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

        # Start waited period with zero
        self.waited_period = 0
        self.current_a = None
        self.total_ever_waited = 0

        # Random if customer has the app
        self.has_app = random.choice([True, False])
        self.goals = self.get_goals()
        self.reached_goals = False

        self.leaving = False
        self.get_walking_distances()

    def get_goals(self):
        """Set random goals."""

        attractions = self.model.get_attractions()
        r = random.randint(1, len(attractions))
        goals = []
        for i in range(r):
            rand_choice = random.choice(attractions)
            goals.append(rand_choice)
            attractions.remove(rand_choice)

        # Sort goals on destination and wating time
        if self.has_app is True:
            pass


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
                possible_steps.remove(obj.pos)

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
                self.model.schedule.remove(self)
                # self.model.grid[self.pos[0]][self.pos[1]] = None
                # TODO: stip ook verwijderen
            else:

                # Only move if there is no queue
                self.model.grid.move_agent(self, new_position)

                self.set_waiting_time()
                self.waiting = True

        # Extra check to see if agent is at destination
        if self.check_move(new_position) is True:
            self.model.grid.move_agent(self, new_position)

    def check_move(self, new_position):
        """ Checks if a move can be done, given a new position."""

        if self.pos == self.destination:
            self.waited_period += 1
            self.total_ever_waited += 1

        # CHANGE DIRECTION if waitingtime is met
        if self.waitingtime is not None:

            if self.waitingtime <= self.waited_period:

                # Update goals and attraction
                for attraction in self.goals:
                    if attraction.pos == self.pos:
                        self.goals.remove(attraction)
                        if attraction.N_current_cust != 1:
                            attraction.N_current_cust -= 1
                        attraction.calculate_waiting_time()

                # Check if agent needs to leave or go to new goal
                if len(self.goals) > 0:
                    self.get_destination()
                else:
                    self.leaving = True
                    self.destination = random.choice(starting_positions)
                    self.waiting = False

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

    def step(self):
        """
        This method should move the customer using the `random_move()` method.
        """
        self.move()

    def get_walking_distances(self):
        """
        Return index of attraction with shortest walking distance.
        _________________________________________________________
        WERKT NOG NIET!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        """
        attractions = self.model.get_attractions()

        distances = {}
        i = 0

        # TODO!!!! DIt even doen,
        for attraction in attractions:
            a = np.array(list(self.pos))
            b = np.array(list(attraction.pos))
            dist = np.linalg.norm(a-b)
            dist = distance.euclidean(a, b)
            distances[i] = dist
            i += 1

        print(distances)
        # Calculate minimum distance
        indexes = []
        {indexes.append(k): v for k, v in sorted(distances.items(), key=lambda item: item[1])}

        # Get index of shortest
        print("Indexes of distance", indexes)

        return indexes

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
        Gives the agent a new destination based on goal and waiting time
        TODO: based on walking distance
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
