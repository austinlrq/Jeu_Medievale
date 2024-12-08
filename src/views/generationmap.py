import tkinter as tk
from perlin_noise import PerlinNoise
import random
from .TYPE import TYPE
from src.views.Case import Case
from math import sqrt
# from src.models import Village  # Import de la classe Village


class GenerateMap:
    def __init__(self, width, height, liste_villages, seed=None):
        self.width = width
        self.height = height
        self.liste_villages = liste_villages
        self.seed = seed
        self.grid = self.generate_map()

    def generate_perlin_noise(self):
        noise1 = PerlinNoise(octaves=3, seed=self.seed)
        noise2 = PerlinNoise(octaves=6, seed=self.seed)
        noise3 = PerlinNoise(octaves=12, seed=self.seed)
        noise4 = PerlinNoise(octaves=24, seed=self.seed)

        pic = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                noise_val = noise1([i / self.height, j / self.width])
                noise_val += 0.5 * noise2([i / self.height, j / self.width])
                noise_val += 0.25 * noise3([i / self.height, j / self.width])
                noise_val += 0.125 * noise4([i / self.height, j / self.width])

                row.append(noise_val)
            pic.append(row)
        return pic

    def place_villages(self):
        random.seed(self.seed)
        village_positions = []
        
        for village in self.liste_villages:
            x_central, y_central = self.random_village_position(village_positions)
            village_positions.append((x_central, y_central))

            village.x = x_central
            village.y = y_central
            village.noble.ajouter_case(self.grid[y_central][x_central])
            
            # Définir la case centrale comme un village
            self.grid[y_central][x_central].type = TYPE.village
            self.grid[y_central][x_central].proprietaire = village.noble
            self.grid[y_central][x_central].village = village
            

            # Définir les zones autour comme des plaines
            for i in range(-2, 3):
                for j in range(-2, 3):
                    if abs(i) + abs(j) <= 2 and abs(i) + abs(j) != 0:
                        new_x, new_y = x_central + i, y_central + j
                        self.grid[new_y][new_x].type = TYPE.plaine
                        self.grid[new_y][new_x].proprietaire = village.noble
                        village.noble.ajouter_case(self.grid[new_y][new_x])                      

    def random_village_position(self, village_positions):
        while True:
            x_central = random.randint(3, self.width - 4) # Pas de spawn trop près des bords
            y_central = random.randint(3, self.height - 4)
            if all(sqrt((x_central - x)**2 + (y_central - y)**2) >= 5 for x, y in village_positions):
                return x_central, y_central

    def generate_map(self):
        perlin_noise = self.generate_perlin_noise()
        map_grid = []
        
        for j in range(self.height):
            row = []
            for i in range(self.width):
                noise_value = perlin_noise[j][i]
                terrain_type = self.determine_terrain(noise_value)
                row.append(Case(i, j, terrain_type))
            map_grid.append(row)
        
        self.grid = map_grid
        self.place_villages()
        return self.grid

    def determine_terrain(self, noise_value):
        if noise_value < -0.4:
            return TYPE.montagneclair
        elif noise_value < -0.25:
            return TYPE.montagne
        elif -0.1 <= noise_value < 0:
            return TYPE.foret
        elif -0.15 <= noise_value < -0.1 or 0 < noise_value <= 0.05:
            return TYPE.foretclair
        elif noise_value > 0.3:
            return TYPE.eau
        elif noise_value > 0.25:
            return TYPE.eauclair
        else:
            return TYPE.plaine

