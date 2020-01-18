from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import numpy as np
from mesa.visualization.ModularVisualization import VisualizationElement
from mesa.visualization.modules import ChartModule

from .model import Themepark
from .customer import Customer
from .route import Route
from .attraction import Attraction

width = 36
height = 36
N_cust = 15
pixel_ratio = 20
num_agents = 6


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
        portrayal["Color"] = "blue"
        portrayal["Shape"] = "circle"

        # portrayal["Shape"] = "attraction.jpg"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 2
        portrayal["r"] = 1
        portrayal["text"] = agent.unique_id

    elif type(agent) is Customer:

        portrayal["text"] = agent.unique_id
        portrayal["text_color"] = "black"
        portrayal["Layer"] = 1

        # Determine if customer has the app or not
        if agent.has_app is True:
            portrayal["Shape"] = "rect"
            portrayal["Color"] = "green"
            portrayal["Filled"] = "true"
            portrayal["w"] = 1
            portrayal["h"] = 1
        else:
            portrayal["Shape"] = "circle"
            portrayal["Filled"] = "true"
            portrayal["r"] = 0.85

        if agent.total_ever_waited > 90:
            portrayal["Color"] = "red"
        elif agent.total_ever_waited > 60:
            portrayal["Color"] = "orange"
        else:
            portrayal["Color"] = "green"

        # UNCOMMENT THIS TO SEE SANNE'S HEAD AS CUSTOMER!
        # portrayal["Shape"] = "starlight.png"

    return portrayal


class HistogramModule(VisualizationElement):
    package_includes = ["Chart.min.js"]
    local_includes = ["HistogramModule.js"]

    def __init__(self, bins, canvas_height, canvas_width):
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.data = []
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


grid = CanvasGrid(agent_draw, width, height, width * pixel_ratio, height * pixel_ratio)

histogram = HistogramModule(["Attraction1", "Attraction2", "Attraction3",
                            "Attraction4", "Attraction5", "Attraction6"], 20, 50)


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
