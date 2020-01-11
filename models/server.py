from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import numpy as np
from mesa.visualization.ModularVisualization import VisualizationElement
from mesa.visualization.modules import ChartModule

from .model import Attraction, Themepark, Customer, Route

NUM_ATTRACTIONS = 3
num_agents = 3


def agent_draw(agent):
    if agent is None:
        return
    portrayal = {}

    if type(agent) is Route:
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "blue"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.15

    elif type(agent) is Attraction:
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "grey"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.9

    elif type(agent) is Customer:
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "red"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.5

    return portrayal


class HistogramModule(VisualizationElement):
    package_includes = ["Chart.min.js"]
    local_includes = ["HistogramModule.js"]

    def __init__(self, bins, canvas_height, canvas_width):
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.bins = ["Attraction1", "Attraction2", "Attraction3"]
        new_element = "new HistogramModule({}, {}, {})"
        new_element = new_element.format(bins,
                                         canvas_width,
                                         canvas_height)
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):

        # TODO, dit moeten dan de echte waardes worden natuurlijk
        wealth_vals = [1, 2, 3]
        hist = np.histogram(wealth_vals, bins=self.bins)[0]
        print("Histogram wordt gemaakt")
        return [int(x) for x in hist]

histogram = HistogramModule(["Attraction1", "Attraction2", "Attraction3"], 200, 500)


width = 26
height = 26
N_attr = 3
N_cust = 5
pixel_ratio = 26

# # width = 10
# # height = 10
# # num_agents = 3
# # pixel_ratio = 10
#
grid = CanvasGrid(agent_draw, width, height, width * pixel_ratio, height * pixel_ratio)
# chart_element = ChartModule([{"Label": "Wolves", "Color": "#AA0000"},
#                              {"Label": "Sheep", "Color": "#666666"}])
server = ModularServer(
    Themepark,
    [grid],

    # om histogram aan te zetten, uncomment dit hier onder
    # [grid, histogram],
    "Theme Park Model",
    {"N_attr": num_agents, "N_cust": N_cust, "width": width, "height": height},
)
server.max_steps = 0
server.port = 8521
