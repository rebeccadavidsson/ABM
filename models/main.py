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
steps = 400
RUNS = 8

memory = [2,3,4,5,6,7,8,9]
# memory = [5,8]
# memory = [5,5,5,5,5,5,5,5]

variation_data = []
for run in range(RUNS):
    print("RUN ", run)
    park = Themepark(num_agents, N_cust, width, height, strategy, theme, steps, memory[run])

    for i in range(steps + 1):
        print("step", i)
        park.step()

    print("Number of run:", run)
    file = pickle.load(open('../data/park_score_mem{}.p'.format(memory[run]), 'rb'))
    variation_data.append(file)

print(variation_data)
pickle.dump(variation_data, open("../data/variation_data_mem{}.p".format(memory[run]), 'wb'))
