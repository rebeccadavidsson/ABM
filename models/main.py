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
theme = "cluster"
strategy = "Closest_by"
strategies = [0, 0.25, 0.5, 0.75, 1, "Random"]
cust_dict, score_dict, hapiness_dict, hist_dict = {}, {}, {}, {}

num_agents = 120
steps = 520
RUNS = 100
strategies = [0, 0.25, 0.5, 0.75, 1, "Random"]


for run in strategies:
    cust_d, score_d, hapiness_d, hist_d = [], [], [], []

    for j in range(RUNS):

        print()
        print("RUN ", j, run)
        print()

        park = Themepark(num_agents, N_cust, width, height, strategy, theme, steps, run)

        for i in range(steps + 1):
            print("step", i)
            park.step()

        cust = pickle.load(open("data/customers.p", 'rb'))
        score = pickle.load(open("data/park_score.p", "rb"))
        hapiness = pickle.load(open("data/hapiness.p", "rb"))
        hist = pickle.load(open("data/cust_history.p", 'rb'))

        cust_d.append(cust)
        score_d.append(score)
        hapiness_d.append(hapiness)
        hist_d.append(hist)

    cust_dict[run] = cust_d
    score_dict[run] = score_d
    hapiness_dict[run] = hapiness_d
    hist_dict[run] = hist_d
    print(score_dict, hapiness_dict)

pickle.dump(cust_dict, open("data/customers_runs.p", 'wb'))
pickle.dump(score_dict, open("data/park_score_runs.p", "wb"))
pickle.dump(hapiness_dict, open("data/hapiness_runs.p", "wb"))
pickle.dump(hist_dict, open("data/cust_history_runs.p", 'wb'))
