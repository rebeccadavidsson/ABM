from mesa import Agent
import random
import math
import numpy as np

class Monitor(Agent):

    def __init__(self, max_time_steps, attraction_positions):
        self.time_dict = make_time_dict(max_time_steps, num_attractions)
        self.attraction_positions = attraction_positions

    def make_time_dict(self, max_time_steps, num_attractions):
        attraction_list = [0] * num_attractions
        dict = {}

        for step in max_time_steps:
            dict[step] = attraction_list
        return dict


    def time_dict_increment(self,next_goal, predicted_arrival_time):

        return self.time_dict[predicted_arrival_time][next_goal] += 1

    def time_dict_decrement(self, attraction, time):

        return self.time_dict[time][attraction] -= 1

    def ETA(current_location, attraction):

        return 0

    def make_prediction(self, current_location, goals):

        return 0
