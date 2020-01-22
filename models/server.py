from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.ModularVisualization import VisualizationElement
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from .model import Themepark
from .customer import Customer
from .route import Route
from .attraction import Attraction

width = 36
height = 36
N_cust = 15
pixel_ratio = 20
num_agents = 7


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
        # portrayal["Filled"] = "false"
        portrayal["Layer"] = 2
        portrayal["r"] = 1
        portrayal["text"] = str(agent.current_waitingtime) + ":" + str(agent.unique_id)
        portrayal["text_color"] = "black"

    elif type(agent) is Customer:

        portrayal["Layer"] = 1

        if agent.waiting is False:
            portrayal["text"] = agent.unique_id
            portrayal["text_color"] = "black"

        # Determine if customer has the app or not
        if agent.has_app is True:
            portrayal["Shape"] = "rect"
            portrayal["Color"] = "green"
            portrayal["Filled"] = "false"
            portrayal["w"] = 0.5
            portrayal["h"] = 0.5
        else:
            portrayal["Shape"] = "circle"
            portrayal["Filled"] = "true"
            portrayal["r"] = 0.65

        if agent.sadness_score > 60:
            portrayal["Color"] = "red"
        elif agent.sadness_score > 40:
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

# class ChartModule(VisualizationElement):
#     package_includes = ["Chart.min.js"]
#     local_includes = ["HistogramModule.js"]
#
#     def __init__(self, canvas_height, canvas_width):
#         self.canvas_height = canvas_height
#         self.canvas_width = canvas_width
#         self.data_collector_name = "datacollector"
#         self.data = []
#         new_element = "new ChartModule({}, {}, {})"
#         new_element = new_element.format(["Attraction1", "Attraction2", "Attraction3"],canvas_width,
#                                          canvas_height,
#                                          self.data)
#         self.js_code = "elements.push(" + new_element + ");"
#
#     def render(self, model):
#         """Render a histogram with HistogramModule.js"""
#
#         data = model.calculate_people()
#         return data

grid = CanvasGrid(agent_draw, width, height, width * pixel_ratio, height * pixel_ratio)

chart = ChartModule([{"Label": "Attraction1", "Color": "#AA0000"},
                    {"Label": "Attraction2", "Color": "#303F9F"},
                    {"Label": "Attraction3", "Color": "#7B1FA2"},
                    {"Label": "Attraction4", "Color": "#D81B60"},
                    {"Label": "Attraction5", "Color": "#2E7D32"},
                    {"Label": "Attraction6", "Color": "#F4511E"},
                    {"Label": "Attraction7", "Color": "#F9A825"}], data_collector_name='datacollector')

histogram = HistogramModule(["Attraction1", "Attraction2", "Attraction3",
                            "Attraction4", "Attraction5", "Attraction6", "Attraction7"], 20, 50)

model_params = {
    "height": height,
    "width": width,
    "N_attr": UserSettableParameter("slider", "Number of attractions", num_agents, 1, num_agents, 1),
    "N_cust": UserSettableParameter("slider", "Number of customers", int(N_cust/1.5), 1, N_cust, 1),
    "strategy": UserSettableParameter('choice', 'Strategy choice', value='Random',
                                      choices=['Random', 'Knowledge', 'Guided']),
}

server = ModularServer(
    Themepark,
    [grid, histogram, chart],
    "Theme Park Model",
    model_params,
)
server.max_steps = 0
server.port = 8521
