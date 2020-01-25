import pickle
import matplotlib.pylab as plt
import numpy as np


file = pickle.load(open('../data/variation_data_c25_a15.p', 'rb'))

arrays = [np.array(x) for x in file]
means = [np.mean(k) for k in zip(*arrays)]

plt.title("Runs=8, Number of customers = 25, number of attractions = 15, type = cluster.")
plt.xlabel("Step")
plt.ylabel("Waiting time")
plt.plot(means)
plt.show()
