from mesa import Agent
import random
from .route import get_coordinates
# from model import calculate_people


WIDTH = 26
HEIGHT = 26

path_coordinates = get_coordinates(WIDTH, HEIGHT)

x_list = [1, int(WIDTH/2), WIDTH-1]
y_list = [int(HEIGHT/2), HEIGHT-1, int(HEIGHT/2)]
positions = [(1, int(HEIGHT/2)), (int(WIDTH/2), HEIGHT-1), (WIDTH-1, int(HEIGHT/2))]



class Customer(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.model = model

        # Assign destination
        self.destination = random.choice(positions)
        while self.destination is self.pos:
            self.destination = random.choice(positions)

        # TODO: Hoe lang blijven de mensen in de attractie?
        self.waitingtime = random.randrange(20, 30)
        self.waiting = False

        # Start waited period with zero
        self.waited_period = 0

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

        # start with random choice of position
        temp = random.choice(possible_steps)

        # Loop over every possible step to get fastest step
        for step in possible_steps:

            # check if step is closer to destination
            if (abs(step[0] - self.destination[0]) < abs(temp[0] - self.destination[0]) or
               abs(step[1] - self.destination[1]) < abs(temp[1] - self.destination[1])):

               temp = step

        new_position = temp

        # Restrict to path
        while new_position not in path_coordinates:
            new_position = self.random.choice(possible_steps)

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

        # Get waitingtime from attraction
        agents = self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            radius=0,
            include_center=True
        )

        for agent_object in agents:
            if type(agent_object) == Attraction:
                self.waitingtime = agent_object.waiting_time

        # CHANGE DIRECTION if waitingtime is met
        if self.waitingtime == self.waited_period:

            # SHORTEST waiting line as destination
            waiting_lines = self.model.calculate_people()

            # Exclude own position
            index_to_exclude = positions.index(self.pos)
            waiting_lines[index_to_exclude] = max(waiting_lines)+1

            # Get minimum watingtime
            minimum = min(waiting_lines)

            # Change current destination to new destination
            self.destination = positions[waiting_lines.index(minimum)]

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
                        if positions[i] != self.pos:
                            self.destination = positions[waiting_lines[i]]
                            break
                else:
                    self.destination = positions[waiting_lines.index(second_shortest)]

            self.waiting = False
            self.waited_period = 0

        if self.waiting is False:
            return True
        return False

    def step(self):
        '''
        This method should move the customer using the `random_move()` method.
        '''
        self.move()
