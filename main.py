"""
OM DEZE TE KUNNEN RUNNEN :
Haal overal de punt weg voor alle imports in customer, route en model.
"""

from mesa import Model, Agent
from models.model import Themepark
import pickle

import os, sys

directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "models"))
sys.path.append(os.path.join(directory, "results"))
sys.path.append(os.path.join(directory, "data"))

width = 36
height = 36
N_cust = 50
pixel_ratio = 20
num_agents = 15
strategy = "Closest_by"
theme = "cluster"
steps = 1000
RUNS = 3

memory = [2,3,4,5,6,7,8,9]
# memory = [5,8]
# memory = [5,5,5,5,5,5,5,5]

variation_data, random_data, close_data = [], [], []

for run in range(RUNS):
    print("RUN ", run)
    park = Themepark(num_agents, N_cust, width, height, strategy, theme, steps, memory[run])

    for i in range(steps + 1):
        print("step", i)
        park.step()

    print("Number of run:", run)

    file = pickle.load(open('data/park_score.p', 'rb'))
    file2 = pickle.load(open('data/strategy_random.p', 'rb'))
    file3 = pickle.load(open('data/strategy_close.p', 'rb'))

    # file = pickle.load(open('../data/park_score_mem{}.p'.format(memory[run]), 'rb'))

    variation_data.append(file)
    random_data.append(file2)
    close_data.append(file3)

pickle.dump(variation_data, open("data/park_scores.p", 'wb'))
pickle.dump(random_data, open("data/random_scores.p", 'wb'))
pickle.dump(close_data, open("data/close_scores.p", 'wb'))

# print(variation_data)
pickle.dump(variation_data, open("data/variation_data_mem{}.p".format(memory[run]), 'wb'))
