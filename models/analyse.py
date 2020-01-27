import pickle
import matplotlib.pylab as plt
import numpy as np
import seaborn as sns
sns.set()

RUNS = 8

# Plot park score over time for each memory size
plt.title("Park Score (Memory 1 to 8)")
for i in range(1, RUNS + 1):
    plt.plot(pickle.load(open('../data/park_score_mem{}.p'.format(i), 'rb')))
plt.ylabel("Park Score")
plt.xlabel("Step")
plt.legend(list(np.arange(1, RUNS + 1)))
plt.show()

# Boxplot for score distributions
data = []
for i in range(1, RUNS + 1):
    data.append(pickle.load(open('../data/park_score_mem{}.p'.format(i), 'rb')))
plt.title("Park Score (Memory 1 to 8)")
plt.boxplot(data)
plt.ylabel("Park Score")
plt.xlabel("Step")
plt.legend(list(np.arange(1, RUNS + 1)))
plt.show()

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
