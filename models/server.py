from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from .model import Customer, Attraction, Themepark
from mesa.visualization.modules import ChartModule


def agent_draw(agent):
    portrayal = None
    if agent is None:
        pass
    elif isinstance(agent, Attraction):
        print("ATTRACTION Uid: {0}, Heading: {1}".format(agent.unique_id, agent.heading))
        portrayal = {
            "Shape": "arrowHead",
            "Filled": "true",
            "Layer": 1,
            "Color": ["#00FF00", "#99FF99"],
            "stroke_color": "#666666",
            "Filled": "true",
            "heading_x": agent.heading[0],
            "heading_y": agent.heading[1],
            "text": agent.unique_id,
            "text_color": "white",
            "scale": 0.8,
        }

    # HIER GAAT HET MIS - hoe verschillende types agents een verschillende portrayal geven?

    # elif isinstance(agent, Customer):
    #     portrayal = None
    #     print("CUSTOMER Uid: {0}, Heading: {1}".format(agent.unique_id, agent.heading))
    #     portrayal = {
    #         "Shape": "circle",
    #         "Filled": "true",
    #         "Layer": 1,
    #         "Color": ["#FFFFFF", "#99FF99"],
    #         "stroke_color": "#666666",
    #         "Filled": "true",
    #         "heading_x": agent.heading[0],
    #         "heading_y": agent.heading[1],
    #         "text": agent.unique_id,
    #         "text_color": "white",
    #         "scale": 0.8,
    #     }

    return portrayal


width = 26
height = 26
N_attr = 3
N_cust = 5
pixel_ratio = 26
grid = CanvasGrid(agent_draw, width, height, width * pixel_ratio, height * pixel_ratio)

chart = ChartModule([{"Label": "Barchart",
                      "Color": "Black"}],
                    data_collector_name='datacollector')

server = ModularServer(Themepark,
                       # [grid, chart],
                       [grid],
                       "Theme Park Model",
                       {"N_attr": N_attr, "N_cust": N_cust, "width": width, "height": height})

# server.max_steps = 0
server.port = 8521
