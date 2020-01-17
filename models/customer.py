from mesa import Agent
import random
from .route import get_coordinates, Route
from .attraction import Attraction
# from model import calculate_people

WIDTH = 36
HEIGHT = 36
NUM_ATTRACTIONS = 5
NUM_OBSTACLES = 20
starting_positions = [[int((WIDTH/2)-1), 0], [int(WIDTH/2), 0], [int((WIDTH/2)+1), 0]]


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

        self.waitingtime = None
        self.waiting = False

        # Start waited period with zero
        self.waited_period = 0
        self.current_a = None

        # Set random goals
        attractions = self.model.get_attractions()
        r = random.randint(1, len(attractions))
        goals = []
        for i in range(r):
            rand_choice = random.choice(attractions)
            goals.append(rand_choice)
            attractions.remove(rand_choice)
        self.goals = goals
        self.reached_goals = False

        self.leaving = False

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

            if self.leaving is True:

                self.model.schedule.remove(self)
                # TODO: stip ook verwijderen
            else:
                # TODO: is dit de goede plek om deze aan te roepen?
                # Sanne: jaaaa, ik had onder de douche ook al bedacht dat die zo kon hihihi
                self.set_waiting_time()

                self.model.grid.move_agent(self, new_position)
                self.waiting = True

        # Extra check to see if agent is at destination
        if self.check_move(new_position) is True:
            self.model.grid.move_agent(self, new_position)


    def check_move(self, new_position):
        """ Checks if a move can be done, given a new position."""

        if self.pos == self.destination:
            self.waited_period += 1

        # CHANGE DIRECTION if waitingtime is met
        if self.waitingtime == self.waited_period:

            # Update goals
            for attraction in self.goals:
                if attraction.pos == self.pos:
                    self.goals.remove(attraction)

            # Check if agent needs to leave or go to new goal
            if len(self.goals) > 0:
                self.get_destination()
            else:
                # TODO: agent has to leave the park
                # print("AGENT SHOULD LEAVE")
                # get leave positions
                # choose a random leave position to go to
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

    def get_destination(self):
        '''
        Gives the agent a new destination based on goal and waiting time
        TODO: based on walking distance
        '''

        # TODO hihi even gehardcoded dit, als jullie dat te lelijk vinden mag het anders
        if len(self.goals) == 1:
            self.destination == self.goals[0].pos
            self.goals = []
        else:
            # TODO: current_waitingtime in attracties updaten

            destinations = []
            for attraction in self.goals:
                # time_to_wait = attraction.current_waitingtime
                # waiting_lines.append(time_to_wait)
                destinations.append(attraction)

            # Get minimum watingtime
            waiting_lines = []
            for destination in destinations:
                waiting_lines.append(destination.current_waitingtime)
            minimum = min(waiting_lines)

            # Change current destination to new destination
            # self.destination = positions[waiting_lines.index(minimum)]
            self.destination = destinations[waiting_lines.index(minimum)].pos

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
                            self.destination = positions[i]
                            break
                else:
                    self.destination = self.positions[waiting_lines.index(second_shortest)]

        self.waiting = False
        self.waited_period = 0
