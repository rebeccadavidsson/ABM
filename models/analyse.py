import pickle
import matplotlib.pylab as plt
import numpy as np


file2 = pickle.load(open('data/strategy_close.p', 'rb'))
file = pickle.load(open('data/strategy_random.p', 'rb'))

plt.plot(file)
plt.plot(file2)
plt.legend(["Random", "Closest_by"])
plt.show()

# arrays = [np.array(x) for x in file]
# means = [np.mean(k) for k in zip(*arrays)]
#
# plt.title("Runs=8, Number of customers = 25, number of attractions = 15, type = cluster.")
# plt.xlabel("Step")
# plt.ylabel("Waiting time")
# plt.plot(means)
# plt.show()
