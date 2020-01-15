from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import numpy as np
from mesa.visualization.ModularVisualization import VisualizationElement
from mesa.visualization.modules import ChartModule

from .model import Themepark
from .customer import Customer
from .route import Route
from .attraction import Attraction

NUM_ATTRACTIONS = 3
num_agents = 3


def agent_draw(agent):
    if agent is None:
        return
    portrayal = {}

    if type(agent) is Route:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "grey"
        portrayal["Filled"] = "true"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Layer"] = 0
        # portrayal["r"] = 0.15

    elif type(agent) is Attraction:
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "gold"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 1
        portrayal["r"] = 1

    elif type(agent) is Customer:
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "red"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.45

    return portrayal


class HistogramModule(VisualizationElement):
    package_includes = ["Chart.min.js"]
    local_includes = ["HistogramModule.js"]

    def __init__(self, bins, canvas_height, canvas_width):
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.bins = ["Attraction1", "Attraction2", "Attraction3"]
        self.data = [] # TODO
        new_element = "new HistogramModule({}, {}, {}, {})"
        new_element = new_element.format(bins,
                                         canvas_width,
                                         canvas_height,
                                         self.data)
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        """Render a histogram with HistogramModule.js"""

        data = model.calculate_people()
        return data


width = 26
height = 26
N_attr = 3
N_cust = 15
pixel_ratio = 26


grid = CanvasGrid(agent_draw, width, height, width * pixel_ratio, height * pixel_ratio)
# chart_element = ChartModule([{"Label": "Wolves", "Color": "#AA0000"},
#                              {"Label": "Sheep", "Color": "#666666"}])

histogram = HistogramModule(["Attraction1", "Attraction2", "Attraction3"], 20, 50)


server = ModularServer(
    Themepark,
    # [grid],

    # om histogram aan te zetten, uncomment dit hier onder
    [grid, histogram],
    "Theme Park Model",
    {"N_attr": num_agents, "N_cust": N_cust, "width": width, "height": height},
)
server.max_steps = 0
server.port = 8521
