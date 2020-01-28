"""
OM DEZE TE KUNNEN RUNNEN :
Haal overal de punt weg voor alle imports in customer, route en model.
"""
import numpy as np
from mesa import Model, Agent
try:
    from .model import Themepark
except ModuleNotFoundError:
    from model import Themepark
import pickle

width = 36
height = 36
N_cust = 50
pixel_ratio = 20
num_agents = 12
theme = "cluster"
strategy = "Closest_by"
steps = 300
RUNS = 5
strategies = [0, 0.25, 0.5, 0.75, 1, "Random"]
strategy_data = {}
hapiness_data = {}

for run in strategies:
    variation_data, hapiness_scores = [], []

    for j in range(RUNS):
        print("RUN ", j, run)
        park = Themepark(num_agents, N_cust, width, height, strategy, theme, steps, run)

        for i in range(steps + 1):
            print("step", i)
            park.step()

        print("Number of run:", run)

        score = pickle.load(open("data/park_score.p", 'rb'))
        hapiness = pickle.load(open("data/hapiness.p", 'rb'))

        variation_data.append(score)
        hapiness_scores.append(hapiness)

    strategy_data[run] = variation_data
    hapiness_data[run] = hapiness_scores
    print(strategy_data, hapiness_data)

pickle.dump(strategy_data, open("data/park_scores.p", 'wb'))
pickle.dump(hapiness_data, open("data/hapiness_scores.p", 'wb'))

# print(variation_data)
# pickle.dump(variation_data, open("../data/variation_data_mem{}.p".format(memory[run]), 'wb'))
