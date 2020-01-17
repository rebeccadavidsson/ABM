from mesa import Agent
import random
from .route import get_coordinates, get_attraction_coordinates
from .attraction import Attraction
from .route import Route
# from model import calculate_people


WIDTH = 36
HEIGHT = 36
NUM_ATTRACTIONS = 5
NUM_OBSTACLES = 20


class Customer(Agent):
    def __init__(self, unique_id, model, pos, x_list, y_list, positions):
        super().__init__(unique_id, model)
        self.pos = pos
        self.model = model
        self.unique_id = unique_id
        self.x_list = x_list
        self.y_list = y_list
        self.positions = positions

        # Assign destination
        self.destination = random.choice(positions)
        while self.destination is self.pos:
            self.destination = random.choice(positions)

        # TODO: Hier gaat iets gek, als waitingtime wordt aangepast (hier) dan
        # veranderd er iets in hoe de customers lopen. Volgens mij had annemijn
        # ook al hier een gekke bug bij.
        self.waitingtime = random.randrange(20, 30)
        # self.waitingtime = 0
        self.waiting = False

        # Start waited period with zero
        self.waited_period = 0
        self.current_a = None

        # Set goals
        # self.goals = pak random attracties
        # self.reached_goals = False

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
        temp_list = []

        # Loop over every possible step to get fastest step
        for step in possible_steps:

            # check if step is closer to destination
            if (abs(step[0] - self.destination[0]) < abs(temp[0] - self.destination[0]) or
               abs(step[1] - self.destination[1]) < abs(temp[1] - self.destination[1])):

               temp = step
               temp_list.append(temp)

        new_position = temp

        if new_position == self.destination and self.waiting is False:

            self.model.grid.move_agent(self, new_position)
            self.waiting = True

        # Extra check to see if agent is at destination
        if self.check_move(new_position) is True:
            self.model.grid.move_agent(self, new_position)

    def check_move(self, new_position):
        """ Checks if a move can be done, given a new position."""

        if self.pos == self.destination:
            self.waited_period += 1

        # TODO: dit kan weg, maar verwijderen is altijd pijnlijk
        # Get waitingtime from attraction
        # agents = self.model.grid.get_neighbors(
        #     self.pos,
        #     moore=True,
        #     radius=0,
        #     include_center=True
        # )
        #
        # for agent_object in agents:
        #     if type(agent_object) == Attraction:
        #         self.waitingtime = agent_object.waiting_time

        # CHANGE DIRECTION if waitingtime is met
        if self.waitingtime == self.waited_period:
            # SHORTEST waiting line as destination
            waiting_lines = self.model.calculate_people()

            # Get minimum watingtime
            minimum = min(waiting_lines)

            # Change current destination to new destination
            self.destination = self.positions[waiting_lines.index(minimum)]

            # If new destination is current attraction choose second closest
            if self.pos == self.destination:
                second_shortest = sorted(waiting_lines)[1]

                # check if two waiting times are of same length
                indexi = []
                for i in range(len(waiting_lines)):
                    if waiting_lines[i] == second_shortest:
                        indexi.append(i)
                if len(indexi) > 1:
                    for i in indexi:
                        if self.positions[i] != self.pos:
                            self.destination = self.positions[i]
                            break
                else:
                    self.destination = self.positions[waiting_lines.index(second_shortest)]

            self.waiting = False
            self.waited_period = 0
            self.current_a = None

        if self.waiting is False:
            return True
        return False

    def set_waiting_time(self):
        '''
        This method calculates the waiting time of the customer based on the
        number of customers in line, and the duration of the attraction
        '''
        # get number of customers in line
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
        '''
        This method should move the customer using the `random_move()` method.
        '''
        self.move()
