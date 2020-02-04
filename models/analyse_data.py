import pickle
import matplotlib.pylab as plt
from matplotlib.lines import Line2D
import numpy as np
import seaborn as sns
import matplotlib.ticker as ticker
sns.set()

RUNS = 100
STRATEGIES = ["Random", "0.00", "0.25", "0.50", "0.75", "1.00"]


def plot_boxplots():
    data = pickle.load(open('results/results_cust_all_only_strat31jan/cust_history_clust_all_only_strat.p', 'rb'))
    df = pd.DataFrame(data)
    print(df["Random"][0][0])
    print(np.sum(df["Random"][0][0]))

    for
    quit()

plot_boxplots()


def plot_strategies():
    """
    Transform data and plot strategies
    """
    try:
        file = pickle.load(open('res_cust_all_only/strategy_history_clust_all_only_strat.p', 'rb'))
        file = pickle.load(open('data/strategy_history_clusterd_diff_strat.p', 'rb'))
        file2 = pickle.load(open('data_all_only_strat/strategy_history.p', 'rb'))
    except:
        file = pickle.load(open('../data/stategy_history_cluster.p', 'rb'))
        file2 = pickle.load(open('../data/stategy_history_circle.p', 'rb'))
    files = [file, file2]

    # for nr, file in enumerate(files):
    for nr in range(1):

        file = files[0]

        # fig, axs = plt.subplots(len(files))
        df = pd.DataFrame(file)
        print(df[0])
        print("------------------",len(df[0]))
        # means = {"0.00": [0] * 520, "0.25": [0] * 520, "0.50": [0] * 520, "0.75": [0] * 520, "1.00": [0] * 520}
        means = {"0.00": [0] * 520, "0.25": [0] * 520, "0.50": [0] * 520, "0.75": [0] * 520, "1.00": [0] * 520}
        # loop over all datasets in df
        for i in range(len(df[0])):

            # show all cols in dataset (0.00, 0.25, 0.50, 0.75, 1.00)
            for col in df[0][i]:

                # put data in matrix depending on their column
                for k, val in enumerate(list(df[0][i][col])):
                    means[col][k] += val

        for key in means:
            key_content = means[str(key)]

            for i in range(len(key_content)):
                means[str(key)][i] = key_content[i] / 65

            print(nr)
            # axs[nr].plot(means[str(key)])
            plt.plot(means[str(key)])

    plt.title("Strategy adaptation over time", fontsize=16)
    # plt.rc("figure", titlesize = 17)
    plt.xlabel("Time (steps)", fontsize=14)
    plt.ylabel("Amount of customers", fontsize=14


    plt.legend(["0.00", "0.25", "0.50", "0.75", "1.00"])
    plt.show()



def plot_themepark_score():
    data = pickle.load(open('results/results_cust_all_only_strat31jan/park_score_clust_all_only_strat.p', 'rb'))
    data2 = [1098, 1093, 1089, 1101, 1084, 1096, 1104, 1118, 1092, 1093, 1102, 1097, 1072, 1064, 1112, 1078, 1100, 1078, 1095, 1108, 1121, 1069, 1079, 1072, 1067, 1072, 1090, 1086, 1057, 1102, 1106, 1051, 1082, 1080, 1108, 1098, 1125, 1068, 1092, 1081, 1097, 1108, 1074, 1110, 1119, 1086, 1085, 1110, 1078, 1086, 1047, 1057, 1121, 1139, 1107, 1072, 1102, 1121, 1114, 1063, 1119, 1156, 1146, 1099, 1067]
    data3 = pickle.load(open('results/results_cust_all_only_strat31jan/park_score.p', 'rb'))
    data4 = pickle.load(open('results/results_cust_all_only_strat31jan/park_score_clusterd_diff_strat.p', 'rb'))

    STRATEGIES = ["Adaptive", "Noise", "Random", "0.00", "0.25", "0.50", "0.75", "1.00"]

    x_pos = np.arange(len(STRATEGIES))
    values = data.values()
    values = list(values)

    total = []
    total.append(data4)
    total.append(data2)
    total.append(values[0])
    total.append(values[1])
    total.append(values[2])
    total.append(values[3])
    total.append(values[4])
    total.append(values[5])

    ticks = STRATEGIES
    fig, axes = plt.subplots()

    boxplot = axes.boxplot(total, patch_artist=True, widths=0.8)
    plt.xticks(x_pos + 1, STRATEGIES)

    # adding horizontal grid lines
    axes.yaxis.grid(True)
    plt.axvline(x=3.5,color='gray',linestyle='--')
    # plt.yticks(np.arange(0, 100, 20))
    # axes.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: ('%g') % (x / 1160)))
    axes.set_title("Park score")
    axes.set_xlabel('Strategy')
    axes.set_ylabel('Score')
    plt.show()


def plot_efficiency_score():
    file = pickle.load(open('results/results_cust_all_only_strat31jan/eff_score_clust_all_only_strat.p', 'rb'))
    file2 = pickle.load(open('results/results_cust_all_only_strat31jan/eff_score_clusterd_diff_strat.p', 'rb'))

    arrays = [np.array(x) for x in file["Random"]]
    means = [np.mean(k) for k in zip(*arrays)]
    arrays = [np.array(x) for x in file[0]]
    means2 = [np.mean(k) for k in zip(*arrays)]
    arrays = [np.array(x) for x in file[0.25]]
    means3 = [np.mean(k) for k in zip(*arrays)]
    arrays = [np.array(x) for x in file[0.5]]
    means4 = [np.mean(k) for k in zip(*arrays)]
    arrays = [np.array(x) for x in file[0.75]]
    means5 = [np.mean(k) for k in zip(*arrays)]
    arrays = [np.array(x) for x in file[1]]
    means6 = [np.mean(k) for k in zip(*arrays)]

    plt.title("Park efficiency score")
    plt.plot(means)
    plt.plot(means2)
    plt.plot(means3)
    plt.plot(means4)
    plt.plot(means5)
    plt.plot(means6)
    plt.xlabel("Timestep")
    plt.ylabel("Score")
    # plt.ylim(0.3,1)
    plt.legend(STRATEGIES)
    plt.show()


    x_pos = np.arange(len(STRATEGIES))
    plt.title("Park efficiency")
    plt.ylabel("Score")
    plt.bar(STRATEGIES, [np.mean(means), np.mean(means2), np.mean(means3), np.mean(means4), np.mean(means5), np.mean(means6)])
    plt.xticks(x_pos, STRATEGIES)
    plt.ylim(0.3,0.9)
    plt.show()


def plot_strategy_hist_clust():
    file = pickle.load(open('results/results_cust_all_only_strat31jan/strategy_history_clusterd_diff_strat.p', 'rb'))

    STRATEGIES = ["0.00", "0.25", "0.50", "0.75", "1.00"]
    data = {}
    for strat in STRATEGIES:
        data[strat] = []
    for line in file:

        for strat in STRATEGIES:

            # Get last value in the list
            data[strat].append(line.iloc[RUNS - 1][strat])

    x_pos = np.arange(len(STRATEGIES))
    values = data.values()
    values = list(values)

    total = []
    total.append(values[0])
    total.append(values[1])
    total.append(values[2])
    total.append(values[3])
    total.append(values[4])

    # fill with colors
    colors = ["lightgreen", "lightblue", "lightgreen", "lightblue", "lightgreen", "lightblue", "lightgreen", "lightblue", "lightgreen", "lightblue"]
    ticks = STRATEGIES
    fig, axes = plt.subplots()

    boxplot = axes.boxplot(total, patch_artist=True, widths=0.8)
    plt.xticks(x_pos + 1, STRATEGIES)
    plt.yticks(np.arange(0, 100, 20))

    colors = ['lightblue', 'lightblue', 'lightblue', "lightblue", "lightblue"]

    for patch, color in zip(boxplot['boxes'], colors):
        patch.set_facecolor(color)

    # adding horizontal grid lines
    axes.yaxis.grid(True)
    axes.set_title("Ratio of people with a specific strategy at the end of a run")
    axes.set_xlabel('Strategy')
    axes.set_ylabel('Percentage of people')
    plt.show()

    total2 = []

    total2.append(round(np.mean(values[0]), 1))
    total2.append(round(np.mean(values[1]), 1))
    total2.append(round(np.mean(values[2]), 1))
    total2.append(round(np.mean(values[3]), 1))
    total2.append(round(np.mean(values[4]), 1))

    plt.title("Ratio of strategies at end of run")
    plt.pie(total2, autopct='%1.1f%%')
    plt.legend(STRATEGIES)
    plt.show()



def plot_eff():
    file = pickle.load(open('results/results_cust_all_only_strat31jan/eff_score_clust_all_only_strat.p', 'rb'))
    file2 = pickle.load(open('results/results_cust_all_only_strat31jan/eff_score_clusterd_diff_strat.p', 'rb'))

    arrays = [np.array(x) for x in file["Random"]]
    means = [np.mean(k) for k in zip(*arrays)]
    arrays = [np.array(x) for x in file[0]]
    means2 = [np.mean(k) for k in zip(*arrays)]
    arrays = [np.array(x) for x in file[0.25]]
    means3 = [np.mean(k) for k in zip(*arrays)]
    arrays = [np.array(x) for x in file[0.5]]
    means4 = [np.mean(k) for k in zip(*arrays)]
    arrays = [np.array(x) for x in file[0.75]]
    means5 = [np.mean(k) for k in zip(*arrays)]
    arrays = [np.array(x) for x in file[1]]
    means6 = [np.mean(k) for k in zip(*arrays)]

    file = file2

    # arrays = [np.array(x) for x in file[0]]
    # meansq = [np.mean(k) for k in zip(*arrays)]
    # arrays = [np.array(x) for x in file[1]]
    # means2q = [np.mean(k) for k in zip(*arrays)]

    plt.title("Park efficiency score")
    plt.xlabel("Timestep")
    plt.ylabel("Score")
    # plt.legend(STRATEGIES)

    plt.boxplot([means, means2, means3, means4, means5, means6])
    plt.show()


def plot_strategy_hist():
    # file = pickle.load(open('results/strategy_history_clusterd_only_random.p', 'rb'))
    # file2 = pickle.load(open('data/all_circle_data_28/stategy_history_circle.p', 'rb'))
    file = pickle.load(open('results/results_cust_all_only_strat31jan/strategy_history_clust_main_rand.p', 'rb'))

    STRATEGIES = ["Random", "0.00", "0.25", "0.50", "0.75", "1.00"]
    data = {}
    for strat in STRATEGIES:
        data[strat] = []
    for line in file:

        for strat in STRATEGIES:

            # Get last value in the list
            data[strat].append(line.iloc[RUNS - 1][strat])

    STRATEGIES = ["0.00", "0.25", "0.50", "0.75", "1.00"]
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


plot_eff()
plot_themepark_score()
plot_efficiency_score()
plot_strategy_hist()
plot_strategy_hist_clust()
