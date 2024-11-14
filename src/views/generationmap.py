import tkinter as tk
from perlin_noise import PerlinNoise
import random
from ..views.Type import TYPE
from ..views.case import Case
from math import sqrt


class Map:
    def __init__(self, width, height, liste_joueur, seed=None):
        self.width = width
        self.height = height
        self.liste_joueur = liste_joueur
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
        
        for _ in range(len(self.liste_joueur)):
            x_central, y_central = self.random_village_position(village_positions)
            village_positions.append((x_central, y_central))
            
            owner = self.liste_joueur.pop()
            self.grid[x_central][y_central].type = TYPE.village
            self.grid[x_central][y_central].proprio = owner

            # Define surrounding area as plains
            for i in range(-2, 3):
                for j in range(-2, 3):
                    if abs(i) + abs(j) <= 2 and abs(i) + abs(j) != 0:
                        new_x, new_y = x_central + i, y_central + j
                        self.grid[new_x][new_y].type = TYPE.plaine
                        self.grid[new_x][new_y].proprio = owner

    def random_village_position(self, village_positions):
        while True:
            x_central = random.randint(3, self.height - 4)
            y_central = random.randint(3, self.width - 4)
            if all(sqrt((x_central - x)**2 + (y_central - y)**2) >= 4 for x, y in village_positions):
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

    def show_map(self, cell_size):
        root = tk.Tk()
        root.title("Carte")
        
        canvas = tk.Canvas(root, height=self.height * cell_size, width=self.width * cell_size)
        canvas.pack()

        colors = {
            TYPE.plaine: "palegoldenrod",
            TYPE.montagne: "gray",
            TYPE.montagneclair: "lightgray",
            TYPE.eau: "steelblue",
            TYPE.eauclair: "lightskyblue",
            TYPE.foret: "darkgreen",
            TYPE.foretclair: "forestgreen",
            TYPE.village: "brown"
        }

        for row in self.grid:
            for cell in row:
                color = colors.get(cell.type, "white")
                x0, y0 = cell.x * cell_size, cell.y * cell_size
                x1, y1 = x0 + cell_size, y0 + cell_size
                canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

                if cell.proprio and cell.type != TYPE.village:
                    step = 10
                    for k in range(0, cell_size + 1, step):
                        canvas.create_line(x0 + k, y0, x0, y0 + k, fill=cell.proprio.couleur, width=1)
                        canvas.create_line(x1 - k, y1, x1, y1 - k, fill=cell.proprio.couleur, width=1)

        root.mainloop()

# Example usage
# width = 60
# height = 40
# nb_village = 2
# seed = 15153
# cell_size = 10
# P1 = Seigneur("main", "cara", 18, 120, 5, 200, "red")
# P2 = Seigneur("bot", "cara", 18, 120, 5, 200, "violet")
# liste_joueur = [P1, P2]

# game_map = Map(width, height, nb_village, liste_joueur, seed)
# game_map.show_map(cell_size)
