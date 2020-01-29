import pickle
import matplotlib.pylab as plt
import numpy as np
import seaborn as sns
import pandas as pd
sns.set()

# data = {0: [446, 390, 413, 435, 387], 0.25: [453, 375, 407, 397, 394], 0.5: [418, 422, 416, 389, 471], 0.75: [412, 415, 437, 451, 417], 1: [415, 396, 435, 424, 426]}
# data2 = {0: [5.957641204754623, 4.994405392734679, 5.762115080302225, 6.572300482168601, 5.21518499265326], 0.25: [4.71287197513577, 5.476524434514284, 6.613457071961583, 5.080424884704873, 6.09731745411721], 0.5: [5.745025484526586, 6.508364300615824, 6.007355090963852, 5.159799785657042, 5.440491978543196], 0.75: [5.733864594465221, 6.003171544955535, 4.898015523753619, 6.347532029728398, 5.776858213075931], 1: [5.673771065932856, 5.5550717964445235, 5.588957298417885, 4.789181645043308, 5.5561914589096775]}
# strategies = [0, 0.25, 0.5, 0.75, 1]
# x_pos = np.arange(len(strategies))
# values = data.values()
# temp = []
# for x in values:
#     temp.append(np.mean(x))
#
# values = data2.values()
# temp2 = []
# for x in values:
#     temp2.append(np.mean(x))
#
# temp = [float(i)/max(temp) for i in temp]
# temp2 = [float(i)/max(temp2) for i in temp2]
# plt.title("Theme park score for different strategies")
# plt.xlabel("Strategy (ratio waitingtime/distance)")
# plt.ylabel("Themepark score")
# plt.ylim(0.9, 1)
# plt.xticks(x_pos, strategies)
# plt.bar(x_pos+0.5, temp, width=0.4)
# plt.bar(x_pos, temp2, width=0.4)
# plt.legend(["Theme park score", "Customer hapiness"])
# plt.show()


# try:
#     file = pickle.load(open('data/stategy_history_cluster.p', 'rb'))
#     file2 = pickle.load(open('data/stategy_history_circle.p', 'rb'))
# except:
#     file = pickle.load(open('../data/stategy_history_cluster.p', 'rb'))
#     file2 = pickle.load(open('../data/stategy_history_circle.p', 'rb'))
# df = pd.DataFrame(file)
# # print(df)
# df.describe()
# # print(df[0].mean())








# x = np.random.rayleigh(50, size=5000)
# y = np.random.rayleigh(50, size=5000)
#
#
# plt.hist2d(x,y, bins=[np.arange(0,400,5),np.arange(0,300,5)])
#
# plt.show()

# Plot park score over time for each memory size
# plt.title("Park Score (Memory 1 to 8)")
# for i in range(1, RUNS + 1):
#     plt.plot(pickle.load(open('../data/park_score_mem{}.p'.format(i), 'rb')))
# plt.ylabel("Park Score")
# plt.xlabel("Step")
# plt.legend(list(np.arange(1, RUNS + 1)))
# plt.show()

# Plot fraction of occupied rides (all_rides_list)
plt.title("All rides")
# for i in range(1, RUNS + 1):
plt.plot(pickle.load(open('../data/all_rides.p', 'rb')))
plt.ylabel("Fraction of occupied rides")
plt.xlabel("Time")
# plt.legend(list(np.arange(1, RUNS + 1)))

plt.show()

# # Boxplot for score distributions
# data = []
# for i in range(1, RUNS + 1):
#     data.append(pickle.load(open('../data/park_score_mem{}.p'.format(i), 'rb')))
# plt.title("Park Score (Memory 1 to 8)")
# plt.boxplot(data)
# plt.ylabel("Park Score")
# plt.xlabel("Step")
# plt.legend(list(np.arange(1, RUNS + 1)))
# plt.show()

# file2 = pickle.load(open('../data/variation_data_c25_a15.p', 'rb'))
# file = pickle.load(open('../data/variation_data_c50_a15.p', 'rb'))
#
# plt.title("Memory = 5")
# plt.plot(file)
# plt.plot(file2)
# plt.ylabel("Waitingtime")
# plt.xlabel("Step")
# plt.legend(["Random", "Closest_by"])
# plt.show()

# arrays = [np.array(x) for x in file]
# means = [np.mean(k) for k in zip(*arrays)]
#
# plt.title("Runs=8, Number of customers = 25, number of attractions = 15, type = cluster.")
# plt.xlabel("Step")
# plt.ylabel("Waiting time")
# plt.plot(means)
# plt.show()



# file = pickle.load(open('../data/variation_data_mem8.p', 'rb'))
# plt.title("Variation (Memory 5 and 8)")
# plt.plot(file)
# plt.ylabel("Park Score")
# plt.xlabel("Step")
# plt.legend()
# plt.show()


#
# file2 = pickle.load(open('data/strategy_close.p', 'rb'))
# file2 = [float(i)/max(file2) for i in file2]
# file = pickle.load(open('data/strategy_random.p', 'rb'))
# file = [float(i)/max(file) for i in file]
# park_score = pickle.load(open('data/park_score.p', 'rb'))
# park_score = [float(i)/max(park_score) for i in park_score]

# plt.title("Memory = 5")
# plt.plot(file)
# plt.plot(file2)
# plt.plot(park_score)
# plt.ylabel("Waitingtime")
# plt.xlabel("Step")
# plt.legend(["N=random", "N=Closest_by", "Waitingtime"])
# plt.show()

# pickle.dump(variation_data, open("data/park_scores.p", 'wb'))
# pickle.dump(random_data, open("data/random_scores.p", 'wb'))
# pickle.dump(close_data, open("data/close_scores.p", 'wb'))

# file2 = pickle.load(open('data/close_scores.p', 'rb'))
# # file2 = [float(i)/max(file2) for i in file2]
# file = pickle.load(open('data/random_scores.p', 'rb'))
# # file = [float(i)/max(file) for i in file]
# park_score = pickle.load(open('data/park_scores.p', 'rb'))
# # park_score = [float(i)/max(park_score) for i in park_score]
#
# arrays = [np.array(x) for x in file]
# means = [np.mean(k) for k in zip(*arrays)]
# # means = [float(i)/max(means) for i in means]
# arrays = [np.array(x) for x in file2]
# means2 = [np.mean(k) for k in zip(*arrays)]
# # means2 = [float(i)/max(means2) for i in means2]
# arrays = [np.array(x) for x in park_score]
# means3 = [np.mean(k) for k in zip(*arrays)]
# # means3 = [float(i)/max(means3) for i in means3]
#
#
# plt.title("Runs=8, Number of customers = 50, number of attractions = 15, type = cluster.")
# plt.xlabel("Step")
# plt.ylabel("Number of people with specific strategy")
# plt.plot(means)
# plt.plot(means2)
# # plt.plot(means3)
# plt.legend(["Closest_by", "Random", "Waitingtime"])
# plt.show()
