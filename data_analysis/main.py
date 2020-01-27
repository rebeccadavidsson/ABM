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
steps = 500
RUNS = 3

variation_data, random_data, close_data = [], [], []
for run in range(RUNS):
    park = Themepark(num_agents, N_cust, width, height, strategy, theme, steps)

    for i in range(steps + 1):
        print("step", i)
        park.step()

    print("Number of run:", run)
    file = pickle.load(open('data/park_score.p', 'rb'))
    file2 = pickle.load(open('data/strategy_random.p', 'rb'))
    file3 = pickle.load(open('data/strategy_close.p', 'rb'))
    variation_data.append(file)
    random_data.append(file2)
    close_data.append(file3)


pickle.dump(variation_data, open("data/park_scores.p", 'wb'))
pickle.dump(random_data, open("data/random_scores.p", 'wb'))
pickle.dump(close_data, open("data/close_scores.p", 'wb'))
