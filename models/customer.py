from mesa import Agent
import random
from .route import get_coordinates


WIDTH = 26
HEIGHT = 26

path_coordinates = get_coordinates(WIDTH, HEIGHT)

x_list = [1, int(WIDTH/2), WIDTH-1]
y_list = [int(HEIGHT/2), HEIGHT-1, int(HEIGHT/2)]
positions = [(1, int(HEIGHT/2)), (int(WIDTH/2), HEIGHT-1), (WIDTH-1, int(HEIGHT/2))]

heading = (1, 0)


class Customer(Agent):
    def __init__(self, unique_id, model, pos, heading=(1, 0)):
        super().__init__(unique_id, model)
        self.pos = pos
        self.model = model
        self.heading = heading
        self.headings = {(1, 0), (0, 1), (-1, 0), (0, -1)}

        # Assign destination
        self.destination = random.choice(positions)
        while self.destination is self.pos:
            self.destination = random.choice(positions)

        # TODO: Hoe lang blijven de mensen in de attractie?
        self.waitingtime = random.randrange(20, 30)

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
        # TODO! Dit moet minder random?
        while new_position not in path_coordinates:
            new_position = self.random.choice(possible_steps)

        # Check if destination has to be changed
        if new_position == self.destination:

            # Let this agent sit in this attraction for a while
            self.waited_period += 1

            if self.waited_period >= self.waitingtime:
                self.destination = random.choice(positions)
                self.waited_period = 0

        elif new_position != self.destination and self.waited_period < self.waitingtime:
            self.model.grid.move_agent(self, new_position)

    def calc_fast_route():
        # volgens mij was het idee om iedere agent een "kaart" met te geven (dict met routes)
        """Calculate fastest route from one attraction to another."""

        pass

    def step(self):
        '''
        This method should move the customer using the `random_move()` method.
        '''
        self.move()
