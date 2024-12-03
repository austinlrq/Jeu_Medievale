import tkinter as tk
from .interface import JeuInterface
from .case import Case
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
        self.selected_villages = []  # Liste des villages sélectionnés
        self.selected_action = None  # Action en cours
        self.case_id_map = {}  # Associe les ID graphiques aux objets Case
        self.territoire_selectionne = []  # Liste des cases sélectionnées
        self.village_affiché = None

        # Canvas pour dessiner la carte
        self.canvas = tk.Canvas(root, width=cols * cell_size, height=rows * cell_size, bg="white")
        self.canvas.pack()

        # Dessiner la grille
        self.draw_grid()
        from src.controllers import GameController
        self.placer_villages(self.gamecontroller.villages)

        self.mettre_a_jour_bordures()
        # Ajouter des événements de clic
        self.canvas.bind("<Button-1>", self.on_click)
        
        # Ajouter un binding pour détecter le clic droit
        self.canvas.bind("<Button-3>", self.clic_droit_village)


    def draw_grid(self):
        """Dessine la grille de la carte et crée des instances de Case."""
        for row in range(self.rows):
            for col in range(self.cols):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                # Crée le rectangle et récupère son ID
                id_case = self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="lightgreen")
                # Créer une instance de Case
                case_instance = Case(row, col)
                # Associe l'ID graphique à l'objet Case
                self.case_id_map[id_case] = case_instance


    def placer_villages(self, villages):
        """Place les villages sur des positions aléatoires de la carte."""
        label_font = font.Font(family="Helvetica", size=7, weight="bold")
        i = 0
        for village in villages:
            while True:
                # Choisir une position aléatoire
                row = random.randint(0, self.rows - 1)
                col = random.randint(0, self.cols - 1)

                # Trouver l'ID de la case correspondante
                case_id = None
                for id_case, case_instance in self.case_id_map.items():
                    if case_instance.row == row and case_instance.col == col:
                        case_id = id_case
                        break

                # Vérifier si la cellule est vide
                if self.case_id_map[case_id].type == "plaine":
                    # Mettre à jour les données de la cellule
                    self.case_id_map[case_id].type = "village"
                    self.case_id_map[case_id].village = village

                    self.gamecontroller.nobles[i].ajouter_case(self.case_id_map[case_id])  # Ajouter la case au noble
                    self.case_id_map[case_id].proprietaire = self.gamecontroller.nobles[i]  # Associer le noble à la case
                    # Mettre à jour le rectangle existant
                    self.canvas.itemconfig(case_id, fill="orange")  # Change la couleur

                    # Ajouter un texte au-dessus du rectangle existant
                    x_center = col * self.cell_size + self.cell_size // 2
                    y_center = row * self.cell_size + self.cell_size // 2
                    self.canvas.create_text(
                        x_center, y_center, text=f"Village {i}", fill="black", font=label_font, tags="cell", state="disabled"
                    )
                    i += 1
                    break

    def on_click(self, event):
        """Gère les clics sur la carte."""
        from src.controllers import GameController
        from src.models import Noble, Seigneur
        # Vérifier si une action est sélectionnée
        if not self.selected_action:
            print("Aucune action sélectionnée.")
            return
        
        # Récupérer l'ID de la case à partir de la position
        id_case = self.canvas.find_withtag("current")  # Récupère l'ID de l'élément cliqué
        if id_case:
            case_instance = self.case_id_map[id_case[0]] # Récupère l'objet Case associé

        if case_instance is None:
            print("Case non trouvée.")
            return
        action_necessitant_village = ["impot", "paysan", "roturier", "immigration"]
        action_necessitant_territoire = ["acheter_case"]

        # Vérifier si la cellule est un village
        village = case_instance.village
        type_case = case_instance.type
        print(type_case, self.selected_action, self.gamecontroller.joueur.possede_case_adjacente(case_instance))
        print(isinstance(self.gamecontroller.joueur,Seigneur))
        if village and self.selected_action in action_necessitant_village:
            print(self.gamecontroller.obtenir_villages_joueur(self.gamecontroller.joueur))
            if village not in self.gamecontroller.obtenir_villages_joueur(self.gamecontroller.joueur):
                print(f"Le village {village.nom} ne vous appartient pas.")
                self.interface.ajouter_evenement("Vous ne possedez pas ce village.")
                return
            if village in self.selected_villages:
                self.selected_villages.remove(village)
                self.unhighlight_cell(case_instance.row, case_instance.col)
                print(f"Village désélectionné : {village.nom}")
            else:
                self.selected_villages.append(village)
                self.highlight_cell(case_instance.row, case_instance.col)
                print(f"Village sélectionné : {village.nom}")
        elif type_case == "plaine" and self.selected_action in action_necessitant_territoire and self.gamecontroller.joueur.possede_case_adjacente(case_instance):
            if case_instance not in self.territoire_selectionne and len(self.territoire_selectionne)==1:
                self.unhighlight_cell(self.territoire_selectionne[0].row, self.territoire_selectionne[0].col)
                self.territoire_selectionne = []
                self.territoire_selectionne.append(case_instance)
                self.highlight_cell(case_instance.row, case_instance.col)
            elif case_instance not in self.territoire_selectionne:
                self.territoire_selectionne.append(case_instance)
                self.highlight_cell(case_instance.row, case_instance.col)
                print(f"Case sélectionnée : ({case_instance.row}, {case_instance.col})")
            elif case_instance in self.territoire_selectionne:
                self.territoire_selectionne.remove(case_instance)
                self.unhighlight_cell(case_instance.row, case_instance.col)
                print(f"Case désélectionnée : ({case_instance.row}, {case_instance.col})")
            else:
                self.territoire_selectionne.remove(case_instance)
                self.unhighlight_cell(case_instance.row, case_instance.col)
                print(f"Case désélectionnée : ({case_instance.row}, {case_instance.col})")
            print("Ceci n'est pas un village.")
        elif type_case == "village" and self.selected_action == "guerre" and self.territoires_adjacents(self.gamecontroller.joueur, case_instance.proprietaire)and case_instance.village not in self.gamecontroller.obtenir_villages_joueur(self.gamecontroller.joueur):
            if self.selected_action not in self.selected_villages and len(self.selected_villages)==1:
                self.unhighlight_cell(self.selected_villages[0].row, self.selected_villages[0].col)
                self.selected_villages = []
                self.territoire_selectionne.append(case_instance)
                self.highlight_cell(case_instance.row, case_instance.col)
            elif case_instance not in self.selected_villages :
                print(case_instance)
                print(self.gamecontroller.obtenir_villages_joueur(self.gamecontroller.joueur))
                self.selected_villages.append(case_instance)
                self.highlight_cell(case_instance.row, case_instance.col)
            else:
                self.selected_villages.remove(case_instance)
                self.unhighlight_cell(case_instance.row, case_instance.col)
                
                print("Vous ne pouvez pas déclarer la guerre")
    
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
            x1, y1, x2, y2, outline="red", width=3, state="disabled"
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
        # Récupérer l'ID de la case à partir de la position
        id_case = self.canvas.find_withtag("current")  # Récupère l'ID de l'élément cliqué
        if id_case:
            case_instance = self.case_id_map[id_case[0]] # Récupère l'objet Case associé

        # Vérifier si un village est associé à la case
        village = case_instance.village  # Méthode pour récupérer le village
        if village:
            self.interface.mettre_a_jour_infos_village(village)
            self.interface.action_bouton_selectionnee = None
            self.village_affiché = village

        def get_village(self, row, col):
            """
            Retourne le village associé à une case donnée (row, col), ou None si vide.
            """
            # Récupérer l'ID de la case à partir de la position
            case_id = None
            for id_case, case_instance in self.case_id_map.items():
                if case_instance.row == row and case_instance.col == col:
                    case_id = id_case
                    break
    
            if case_id is None:
                return None
    
            # Récupérer les données de la cellule
            case_instance = self.case_id_map[case_id]
    
            # Vérifier si la cellule est un village
            village = case_instance.type
            self.village_affiché = village
            return village

    def get_voisins(self, case):
        """Retourne les voisins (haut, bas, gauche, droite) d'une case."""
        voisins = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Haut, bas, gauche, droite
        for d_row, d_col in directions:
            voisin_row = case.row + d_row
            voisin_col = case.col + d_col
            if 0 <= voisin_row < self.rows and 0 <= voisin_col < self.cols:
                for id_case, case_instance in self.case_id_map.items():
                    if case_instance.row == voisin_row and case_instance.col == voisin_col:
                        voisins.append(case_instance)
                        break
        return voisins

    def dessiner_bordures(self, case_id, case):
        """Dessine les bordures uniquement sur les arêtes adjacentes à un territoire différent."""
        voisins = self.get_voisins(case)
        x1, y1, x2, y2 = self.canvas.coords(case_id)  # Coordonnées de la case

        # Supprime d'abord les bordures existantes
        self.canvas.delete(f"border_{case.row}_{case.col}")

        # Détermine la couleur du propriétaire (seigneur ou noble)
        couleur_bordure = case.proprietaire.couleur_bordure if case.proprietaire else "black"

        for voisin in voisins:
            if voisin.proprietaire != case.proprietaire:
                if voisin.row < case.row:  # Haut
                    self.canvas.create_line(x1, y1, x2, y1, fill=couleur_bordure, width=2, tags=f"border_{case.row}_{case.col}")
                elif voisin.row > case.row:  # Bas
                    self.canvas.create_line(x1, y2, x2, y2, fill=couleur_bordure, width=2, tags=f"border_{case.row}_{case.col}")
                elif voisin.col < case.col:  # Gauche
                    self.canvas.create_line(x1, y1, x1, y2, fill=couleur_bordure, width=2, tags=f"border_{case.row}_{case.col}")
                elif voisin.col > case.col:  # Droite
                    self.canvas.create_line(x2, y1, x2, y2, fill=couleur_bordure, width=2, tags=f"border_{case.row}_{case.col}")

    def mettre_a_jour_bordures(self):
        """Met à jour les bordures de toutes les cases."""
        for case_id, case in self.case_id_map.items():
            if case.proprietaire is not None:
                self.dessiner_bordures(case_id, case)
    
    # Guerre
    
    def territoires_adjacents(self, attaquant, defenseur):
        """
        Vérifie si le territoire d'attaquant est adjacent à celui de défenseur.
        """
        for case_id, case in self.case_id_map.items():
            if case.proprietaire == attaquant:
                # Vérifie les voisins de chaque case de l'attaquant
                voisins = self.get_voisins(case)
                for voisin in voisins:
                    if voisin.proprietaire == defenseur:
                        return True  # Adjacence trouvée
        return False  # Aucun territoire adjacent trouvé

