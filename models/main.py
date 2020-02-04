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
theme = "circle"
strategy = "Closest_by"
steps = 10
RUNS = 1
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

    variation_data.append(file)


# TODO: HIER WORDT 2X DEZELFDE WAARDE OPGESLAGEN, BIJ WELKE HOORT DIE ECHT?
pickle.dump(variation_data, open("../data/park_scores.p", 'wb'))

pickle.dump(variation_data, open("../data/variation_data.p", 'wb'))
