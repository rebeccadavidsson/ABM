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
        # TODO! Dit moet minder random?
        while new_position not in path_coordinates:
            new_position = self.random.choice(possible_steps)

        if new_position == self.destination and self.waiting is False:
            self.model.grid.move_agent(self, new_position)
            self.waiting = True

        if self.pos == self.destination:
            self.waited_period += 1

        # TODO: Get waitingtime from attraction, not from customer. Dus model.grid nodig?
        if self.waitingtime == self.waited_period:

            # Change direction
            # TODO: implementeren van de target functie

            # RANDOM new destination
            # temp_new = random.choice(positions)
            # while self.destination == temp_new:
            #     temp_new = random.choice(positions)
            # self.destination = temp_new

            # SHORTEST waiting line as destination
            # TODO: current attraction should not be an option, even if it has the shortest waiting line
            waiting_lines = self.model.calculate_people()
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
