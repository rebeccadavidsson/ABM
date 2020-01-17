# ABM
Agent Based Modelling UvA (2020)

### Requirements
All requirements can be installed with:
```
pip install -r requirements.txt
```

### Repository

* ```run.py```: main file to run. Run with the command:
```
python3 run.py
```
or
```
mesa runserver
```

#### /models

* ```attraction.py```: includes the agent Attraction.
* ```customer.py```: includes the agent Customer and helper functions such as ```get_destination()```.
* ```model.py```: includes the model Themepark and defines the Mesa grid and schedule.
* ```route.py```: calculates coordinates of attractions and adds possible obstacles.
* ```server.py```: launches the mesa visualization.

### Built with
* [Mesa](https://github.com/projectmesa/mesa) - ABM Framework
* [Matplotlib](https://matplotlib.org) - 2D plotting

### Authors
* __R. Davidsson__
* __S. Donker__
* __A. Dijkhuis__
* __R. van Drimmelen__
* __L. Heek__
* __S. Verhezen__

## License
This project is licensed under the GNU General Public License v3.0.
