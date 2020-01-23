import pickle
import matplotlib.pyplot as plt

"""
Assumes following datatypes for results:

Agents:         1. List of integers: number of visited attractions
                2. List of integers: total time spend waiting during run

Attractions:    1. [id, duur ritje, locatie, [aantal customers], [duur wachtrij]]
"""

def histogram_attractions():
    # results = pickle.load(pickle.load(open('<iets.p>', 'rb')))
    avg_res = [[],[]]
    results = [[1, 10, (15,30), [1,1,2,2,3,3,4,4,5,5], [0,1,2,3,4,5,5,5,5,5]],
                [2, 10, (15,30), [1,2,3,4,5,6,7,8,9,10], [0,2,4,6,8,10,8,6,4,2]]]
    leg =[]
    fig, ax = plt.subplots()
    for result in results:
        ax.plot(result[4])
        leg.append("Attraction id " + str(result[0]))
    ax.legend(leg)

    ax.set(xlabel='timepoints (t)', ylabel='length of waiting line (l)',
            title='Waiting lines for attractions')

    # fig.savefig("test.png")
    plt.show()

if __name__ == "__main__":
    histogram_attractions()
