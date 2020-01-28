"""
OM DEZE TE KUNNEN RUNNEN :
Haal overal de punt weg voor alle imports in customer, route en model.
"""

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
num_agents = 15
theme = "cluster"
strategy = "Closest_by"
steps = 100
RUNS = 8

# memory = [2,3,4,5,6,7,8,9]
memory = 5
strategies = [0, 0.25, 0.5, 0.75, 1]


variation_data = []

for run in range(RUNS):
    print("RUN ", run)
    park = Themepark(num_agents, N_cust, width, height, strategy, theme, steps, strategies[run])

    for i in range(steps + 1):
        print("step", i)
        park.step()

    print("Number of run:", run)

    file = pickle.load(open('../data/park_score.p', 'rb'))

    # file = pickle.load(open('../data/park_score_mem{}.p'.format(memory[run]), 'rb'))

    variation_data.append(file)

pickle.dump(variation_data, open("../data/park_scores.p", 'wb'))

# print(variation_data)
pickle.dump(variation_data, open("../data/variation_data_mem{}.p".format(memory[run]), 'wb'))
