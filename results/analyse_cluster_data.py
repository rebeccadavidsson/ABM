import pickle
import matplotlib.pylab as plt
from matplotlib.lines import Line2D
import numpy as np
import seaborn as sns
sns.set()

RUNS = 520


def plot_themepark_score():
    data = pickle.load(open('results/park_score_clusterd_only_random.p', 'rb'))
    plt.boxplot(data)
    plt.show()


def plot_efficiency_score():
    file = pickle.load(open('results/eff_score_clust_main_rand.p', 'rb'))
    arrays = [np.array(x) for x in file]
    means = [np.mean(k) for k in zip(*arrays)]
    plt.plot(means)
    plt.show()


def plot_strategy_hist():
    file = pickle.load(open('results/strategy_history_clusterd_only_random.p', 'rb'))
    file2 = pickle.load(open('data/all_circle_data_28/stategy_history_circle.p', 'rb'))

    STRATEGIES = ["0.00", "0.25", "0.50", "0.75", "1.00"]
    data = {}
    for strat in STRATEGIES:
        data[strat] = []
    for line in file:
        for strat in STRATEGIES:

            # Get last value in the list
            data[strat].append(line.iloc[RUNS - 1][strat])

    data2 = {}
    for strat in STRATEGIES:
        data2[strat] = []
    for line in file2:
        for strat in STRATEGIES:

            # Get last value in the list
            data2[strat].append(line.iloc[RUNS - 1][strat])

    x_pos = np.arange(len(STRATEGIES * 2))
    values = data.values()
    values2 = data2.values()
    values = list(values)
    values2 = list(values2)
    total = []
    total.append(values[0])
    total.append(values2[0])
    total.append(values[1])
    total.append(values2[1])
    total.append(values[2])
    total.append(values2[2])
    total.append(values[3])
    total.append(values2[3])
    total.append(values[4])
    total.append(values2[4])

    # total.append([float(i)/max(values[0]) for i in values[0]])
    # total.append([float(i)/max(values2[0]) for i in values2[0]])
    # total.append([float(i)/max(values[1]) for i in values[1]])
    # total.append([float(i)/max(values2[1]) for i in values2[1]])
    # total.append([float(i)/max(values[2]) for i in values[2]])
    # total.append([float(i)/max(values2[2]) for i in values2[2]])
    # total.append([float(i)/max(values[3]) for i in values[3]])
    # total.append([float(i)/max(values2[3]) for i in values2[3]])
    # total.append([float(i)/max(values[4]) for i in values[4]])
    # total.append([float(i)/max(values2[4]) for i in values2[4]])
    # values = [float(i)/max(values) for i in values]
    # values2 = [float(i)/max(values2) for i in values2]

    # fill with colors
    colors = ["lightgreen", "lightblue", "lightgreen", "lightblue", "lightgreen", "lightblue", "lightgreen", "lightblue", "lightgreen", "lightblue"]
    ticks = STRATEGIES
    fig, axes = plt.subplots()

    boxplot = axes.boxplot(total, patch_artist=True, widths=0.4, positions = [0.7, 1.3, 2.7, 3.3, 4.7, 5.3, 6.7, 7.3, 8.7, 9.3])
    plt.xticks(x_pos + 1, STRATEGIES)
    plt.xticks(range(1, len(ticks) * 2, 2), ticks)
    for patch, color in zip(boxplot['boxes'], colors):
        patch.set_facecolor(color)

    custom_lines = [Line2D([0], [0], color="lightgreen", lw=4),
                    Line2D([0], [0], color="lightblue", lw=4)]

    # adding horizontal grid lines
    axes.yaxis.grid(True)
    axes.set_title("Average number of people with a specific strategy, runs=65")
    axes.set_xlabel('Strategy')
    axes.set_ylabel('Number of people')
    axes.legend(custom_lines, ["Cluster", "Circle"])
    plt.show()



plot_themepark_score()
# plot_efficiency_score()
# plot_strategy_hist()
