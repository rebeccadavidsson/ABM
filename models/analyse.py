import pickle
import matplotlib.pylab as plt
import numpy as np
import seaborn as sns
sns.set()

RUNS = 8

# Plot park score over time for each memory size
# plt.title("Park Score (Memory 1 to 8)")
# for i in range(1, RUNS + 1):
#     plt.plot(pickle.load(open('../data/park_score_mem{}.p'.format(i), 'rb')))
# plt.ylabel("Park Score")
# plt.xlabel("Step")
# plt.legend(list(np.arange(1, RUNS + 1)))
# plt.show()
#
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



file2 = pickle.load(open('data/strategy_close.p', 'rb'))
file2 = [float(i)/max(file2) for i in file2]
file = pickle.load(open('data/strategy_random.p', 'rb'))
file = [float(i)/max(file) for i in file]
park_score = pickle.load(open('data/park_score.p', 'rb'))
park_score = [float(i)/max(park_score) for i in park_score]

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

file2 = pickle.load(open('data/close_scores.p', 'rb'))
# file2 = [float(i)/max(file2) for i in file2]
file = pickle.load(open('data/random_scores.p', 'rb'))
# file = [float(i)/max(file) for i in file]
park_score = pickle.load(open('data/park_scores.p', 'rb'))
# park_score = [float(i)/max(park_score) for i in park_score]

arrays = [np.array(x) for x in file]
means = [np.mean(k) for k in zip(*arrays)]
# means = [float(i)/max(means) for i in means]
arrays = [np.array(x) for x in file2]
means2 = [np.mean(k) for k in zip(*arrays)]
# means2 = [float(i)/max(means2) for i in means2]
arrays = [np.array(x) for x in park_score]
means3 = [np.mean(k) for k in zip(*arrays)]
# means3 = [float(i)/max(means3) for i in means3]


plt.title("Runs=8, Number of customers = 50, number of attractions = 15, type = cluster.")
plt.xlabel("Step")
plt.ylabel("Number of people with specific strategy")
plt.plot(means)
plt.plot(means2)
# plt.plot(means3)
plt.legend(["Closest_by", "Random", "Waitingtime"])
plt.show()
