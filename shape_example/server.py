from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from .model import Attraction, Themepark


def agent_draw(agent):
    portrayal = None
    if agent is None:
        pass
    elif isinstance(agent, Attraction):
        print("Uid: {0}, Heading: {1}".format(agent.unique_id, agent.heading))
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
    return portrayal


width = 26
height = 26
num_agents = 3
pixel_ratio = 26
grid = CanvasGrid(agent_draw, width, height, width * pixel_ratio, height * pixel_ratio)
server = ModularServer(
    Themepark,
    [grid],
    "Theme Park Model",
    {"N": num_agents, "width": width, "height": height},
)
server.max_steps = 0
server.port = 8521
