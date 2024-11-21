import tkinter as tk
from .interface import JeuInterface
from src.controllers import GameController
from tkinter import font
import random

class Map:
    def __init__(self, root, game_controller, rows=10, cols=10, cell_size=50):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.gamecontroller = game_controller

        self.highlighted_cells = {}

        # Structure des données pour stocker les cellules
        self.map_data = [[None for _ in range(cols)] for _ in range(rows)]
        self.selected_villages = []  # Liste des villages sélectionnés
        self.selected_action = None  # Action en cours

        self.village_affiché = None

        # Canvas pour dessiner la carte
        self.canvas = tk.Canvas(root, width=cols * cell_size, height=rows * cell_size, bg="white")
        self.canvas.pack()

        # Dessiner la grille
        self.draw_grid()
        
        self.placer_villages(self.gamecontroller.villages)

        # Ajouter des événements de clic
        self.canvas.bind("<Button-1>", self.on_click)
        
        # Ajouter un binding pour détecter le clic droit
        self.canvas.bind("<Button-3>", self.clic_droit_village)


    def draw_grid(self):
        """Dessine la grille de la carte."""
        for row in range(self.rows):
            for col in range(self.cols):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                # Dessiner un rectangle pour chaque cellule
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="lightgreen")
                # Stocker des informations par défaut dans chaque cellule
                self.map_data[row][col] = {"terrain": "plaine", "objet": None}

    def placer_villages(self, villages):
        """Place les villages sur des positions aléatoires de la carte."""
        label_font = font.Font(family="Helvetica", size=7, weight="bold")
        i=0
        for village in villages:
            while True:
                # Choisir une position aléatoire
                row = random.randint(0, self.rows - 1)
                col = random.randint(0, self.cols - 1)

                # Vérifier si la cellule est vide
                if self.map_data[row][col]["objet"] is None:
                    # Mettre à jour les données de la cellule
                    self.map_data[row][col]["objet"] = village
                    self.map_data[row][col]["terrain"] = "village"
                    village.coords = (row, col)  # Assigner les coordonnées au village

                    # Dessiner le village sur la carte
                    x1 = col * self.cell_size
                    y1 = row * self.cell_size
                    x2 = x1 + self.cell_size
                    y2 = y1 + self.cell_size
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="orange")
                    self.canvas.create_text(
                        (x1 + x2) // 2, (y1 + y2) // 2, text=f"Village {i}", fill="black", font=label_font
                    )
                    i = i + 1
                    break  # Sortir de la boucle après avoir placé le village

    def on_click(self, event):
        """Gère les clics sur la carte."""
        col = event.x // self.cell_size
        row = event.y // self.cell_size

        # Vérifier si une action est sélectionnée
        if not self.selected_action:
            print("Aucune action sélectionnée.")
            return

        # Récupérer les données de la cellule
        cell_data = self.map_data[row][col]
        action_nessecitant_case = ["impot", "paysan", "roturier", "immigration"]
        # Vérifier si la cellule est un village
        village = cell_data["objet"]
        if village and cell_data["terrain"] == "village" and self.selected_action in action_nessecitant_case:
            if village not in self.gamecontroller.obtenir_villages_joueur(self.gamecontroller.joueur):
                print(f"Le village {village.nom} ne vous appartient pas.")
                self.interface.ajouter_evenement("Vous ne possedez pas ce village.")
                return
            if village in self.selected_villages:
                self.selected_villages.remove(village)
                self.unhighlight_cell(row, col)
                print(f"Village désélectionné : {village.nom}")
            else:
                self.selected_villages.append(village)
                self.highlight_cell(row, col)
                print(f"Village sélectionné : {village.nom}")
        else:
            print("Ceci n'est pas un village.")

    def highlight_cell(self, row, col):
        """Met en surbrillance une cellule sélectionnée."""
        if (row, col) in self.highlighted_cells:
            # Si déjà en surbrillance, ne rien faire
            return

        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        # Créer un rectangle rouge autour de la cellule
        rect_id = self.canvas.create_rectangle(
            x1, y1, x2, y2, outline="red", width=3
        )
        self.highlighted_cells[(row, col)] = rect_id  # Stocker l'identifiant

    def unhighlight_cell(self, row, col):
        """Réinitialise une cellule désélectionnée."""
        """x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=1)"""

        if (row, col) in self.highlighted_cells:
            # Supprimer le rectangle rouge
            self.canvas.delete(self.highlighted_cells[(row, col)])
            del self.highlighted_cells[(row, col)]  # Retirer du dictionnaire

    def clic_droit_village(self, event):
        """
        Gère le clic droit sur une case pour afficher les informations du village.
        """
        # Calculer les coordonnées de la case cliquée
        row = event.y // self.cell_size
        col = event.x // self.cell_size

        # Vérifier si un village est associé à la case
        village = self.get_village(event)  # Méthode pour récupérer le village
        if village:
            self.interface.mettre_a_jour_infos_village(village)
            self.interface.immigration_selectionnee = None
        #else:
            #self.interface.mettre_a_jour_infos_village(None)

    def get_village(self, event):
        """
        Retourne le village associé à une case donnée (row, col), ou None si vide.
        """
        col = event.x // self.cell_size
        row = event.y // self.cell_size

        # Récupérer les données de la cellule
        cell_data = self.map_data[row][col]

        # Vérifier si la cellule est un village
        village = cell_data["objet"]
        self.village_affiché = village
        return village
