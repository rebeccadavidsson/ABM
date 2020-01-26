"""
OM DEZE TE KUNNEN RUNNEN :
Haal overal de punt weg voor alle imports in customer, route en model.
"""

from mesa import Model, Agent
from model import Themepark
import pickle

width = 36
height = 36
N_cust = 50
pixel_ratio = 20
num_agents = 15
strategy = "Closest_by"
theme = "cluster"
steps = 250
RUNS = 8

variation_data = []
for run in range(RUNS):
    park = Themepark(num_agents, N_cust, width, height, strategy, theme, steps)

    for i in range(steps + 1):
        print("step", i)
        park.step()

    print("Number of run:", run)
    file = pickle.load(open('../data/park_score.p', 'rb'))
    variation_data.append(file)

print(variation_data)
pickle.dump(variation_data, open("../data/variation_data.p", 'wb'))
