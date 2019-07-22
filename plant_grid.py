#!/usr/bin/env python
"""Plant Grid Farmware"""

import numpy as np
from farmware_tools import get_config_value, app
from farmware_tools.device import log

class Grid():
    'Add a grid of plants to the farm designer.'
    def __init__(self, configs):
        self.x_num = configs['x_num']
        self.y_num = configs['y_num']
        self.x_step = configs['x_step']
        self.y_step = configs['y_step']
        self.x_start = configs['x_start']
        self.y_start = configs['y_start']
        self.radius = configs['radius']
        self.name = configs['name']
        self.slug = configs['slug']
        self.grid_values = self.create_grid()

    def create_grid(self):
        'Create a coordinate grid based on the input options.'
        unit_grid = np.mgrid[0:self.x_num, 0:self.y_num]
        plant_grid = unit_grid
        plant_grid[0] = self.x_start + unit_grid[0] * self.x_step
        plant_grid[1] = self.y_start + unit_grid[1] * self.y_step
        x_values, y_values = np.vstack(list(map(np.ravel, plant_grid)))
        self.x_uniq = sorted(list(set(x_values)))
        self.y_uniq = sorted(list(set(y_values)))
        grid_values = [{'x': int(x), 'y': int(y)} for x, y in zip(x_values, y_values)]
        return grid_values

    def print_coordinates(self):
        'Print a representation of the grid coordinates.'
        fmt = '{:^6}'
        print(fmt.format('') + ''.join([fmt.format(x) for x in self.x_uniq]))
        for y_value in self.y_uniq:
            print(fmt.format(y_value) + fmt.format('*') * len(self.x_uniq))

    def add_plants(self):
        'Add all plants in the grid to the farm designer.'
        for plant in self.grid_values:
            app.add_plant(plant['x'], plant['y'], radius=self.radius,
                          openfarm_slug=self.slug, name=self.name)
        log('{} {} plants added, starting at ({}, {}).'.format(
            len(self.grid_values), self.slug, self.x_start, self.y_start),
            'success')

INT_CONFIG_KEYS = [
    'x_num', 'y_num', 'x_step', 'y_step', 'x_start', 'y_start', 'radius'
    ]

if __name__ == '__main__':
    FARMWARE_NAME = 'Plant Grid'
    # Load inputs from Farmware page specified in manifest file
    CONFIGS = {key: get_config_value(FARMWARE_NAME, key) for key in INT_CONFIG_KEYS}
    CONFIGS['name'] = get_config_value(FARMWARE_NAME, 'name', str)
    CONFIGS['slug'] = get_config_value(FARMWARE_NAME, 'slug', str)

    GRID = Grid(CONFIGS)
    #GRID.print_coordinates()
    GRID.add_plants()
