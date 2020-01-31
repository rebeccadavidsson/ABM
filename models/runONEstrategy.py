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
cust_dict, score_dict, hapiness_dict, hist_dict, strat_dict = {}, {}, {}, {}, {}

num_agents = 12
steps = 100
RUNS = 1
strategies = [0, 0.25, 0.5, 0.75, 1]

# num_agents = 12
# steps = 30
# RUNS = 1
# strategies = [0.5]


for run in strategies:
    cust_d, score_d, hapiness_d, hist_d, strategy_d = [], [], [], [], []

    for j in range(RUNS):

        print()
        print("RUN ", j, run)
        print()

        park = Themepark(num_agents, N_cust, width, height, strategy, theme, steps, run)

        for i in range(steps + 1):
            print("step", i)
            park.step()

        try:
            cust = pickle.load(open("data/customers.p", 'rb'))
            score = pickle.load(open("data/park_score.p", "rb"))
            hapiness = pickle.load(open("data/hapiness.p", "rb"))
            hist = pickle.load(open("data/cust_history.p", 'rb'))
            strategy_hist = pickle.load(open("data/strategy_history.p", 'rb'))
        except:
            cust = pickle.load(open("../data/customers.p", 'rb'))
            score = pickle.load(open("../data/park_score.p", "rb"))
            hapiness = pickle.load(open("../data/hapiness.p", "rb"))
            hist = pickle.load(open("../data/cust_history.p", 'rb'))
            strategy_hist = pickle.load(open("../data/strategy_history.p", 'rb'))

        cust_d.append(cust)
        score_d.append(score)
        hapiness_d.append(hapiness)
        hist_d.append(hist)
        strategy_d.append(strategy_hist)

    cust_dict[run] = cust_d
    score_dict[run] = score_d
    hapiness_dict[run] = hapiness_d
    hist_dict[run] = hist_d
    strat_dict[run] = strategy_d

    print(score_dict, hapiness_dict)
    print(strat_dict)

try:
    pickle.dump(cust_dict, open("results/customers_runs.p", 'wb'))
    pickle.dump(score_dict, open("results/park_score_runs.p", "wb"))
    pickle.dump(hapiness_dict, open("results/hapiness_runs.p", "wb"))
    pickle.dump(hist_dict, open("results/cust_history_runs.p", 'wb'))
    pickle.dump(strategy_hist, open("results/strategy_history.p", 'wb'))
except:
    pickle.dump(cust_dict, open("../results/customers_runs.p", 'wb'))
    pickle.dump(score_dict, open("../results/park_score_runs.p", "wb"))
    pickle.dump(hapiness_dict, open("../results/hapiness_runs.p", "wb"))
    pickle.dump(hist_dict, open("../results/cust_history_runs.p", 'wb'))
    pickle.dump(strategy_hist, open("../results/strategy_history.p", 'wb'))
