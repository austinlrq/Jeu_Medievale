import tkinter as tk
import json
# from .interface import JeuInterface
# from src.controllers import GameController
from tkinter import font
from .generationmap import GenerateMap
import random
from PIL import ImageColor
from .TYPE import TYPE
from .mapdrag import MapDrag
from .mapzoom import MapZoom
from collections import deque


class Map:
    def __init__(self, root, game_controller, interface, case_size=50, map_data = None):
        self.root = root
        self.case_size = case_size
        self.gamecontroller = game_controller
        self.interface = interface

        self.highlighted_cases = {}

        # Structure des données pour stocker les caseules

        self.selected_villages = []  # Liste des villages sélectionnés
        self.selected_action = None  # Action en cours
        self.territoire_selectionne = []
        self.village_affiché = None
        if map_data:
            self.width_map = map_data["width"]
            self.height_map = map_data["height"]
            self.grid = map_data["grid"]
        else:
            self.width_map = 100
            self.height_map = 100
            self.load_info_map()
            self.grid = GenerateMap(self.width_map,self.height_map,self.gamecontroller.villages).grid
        # Cadre pour la carte (grille)
        self.map_frame = tk.Frame(self.root, bg="#2E2E2E")
        self.map_frame.pack(expand=True, fill="both", padx=5, pady=1)
        self.map = map
        
        # Create map and bind mouse events for dragging
        self.creer_grille_carte()
       
        # Ajouter des événements de clic
        self.canvas.bind("<Button-1>", self.on_click)

        # Ajouter un binding pour détecter le controle clic gauche
        self.canvas.bind("<Control-Button-1>", self.clic_gauche_village)

    def load_info_map(self):
        with open("src/settings.json", "r") as f:
           data = json.load(f)
        self.height_map = data["HAUTEUR_MAP"]
        self.width_map = data["LARGEUR_MAP"]

    def creer_grille_carte(self, case_size=50):
        self.map_compenser_x = 0  # Compensateur horizontal de la carte
        self.map_compenser_y = 0  # Compensateur vertical de la carte
        self.debut_x = 0         # Position initiale en x pour le glissement
        self.debut_y = 0         # Position initiale en y pour le glissement
        self.case_size = case_size
        # Create canvas and dynamically calculate the visible dimensions
        self.canvas = tk.Canvas(
            self.map_frame, bg="#2E2E2E", highlightthickness=0
        )
        self.canvas.pack(expand=True, fill="both", anchor="center")
        
        self.nb_colonnes_visibles = self.canvas.winfo_width() // self.case_size
        self.nb_lignes_visibles = self.canvas.winfo_height() // self.case_size
        # Initialiser les gestionnaires pour zoom et drag
        self.zoom_manager = MapZoom(self.canvas, self)
        self.drag_manager = MapDrag(self.canvas, self)
        self.root.update_idletasks()  # Force l'actualisation de la fenêtre
        self.centrer_sur_village()


    def centrer_sur_village(self):
        """Centre la carte sur le village du joueur."""
        # Récupérer les coordonnées du village du joueur
        village_coords = (0,0)
        for village in self.gamecontroller.villages:
            if village.noble == self.gamecontroller.joueur:
                village_coords = village.get_coords()
                break

        if not village_coords:
            print("Aucun village trouvé pour centrer la carte.")
            return

        village_x, village_y = village_coords

        # Calculer les nouveaux compensateurs pour centrer le village
        nouveau_compenser_x = max(0, village_x - self.nb_colonnes_visibles // 2)
        nouveau_compenser_y = max(0, village_y - self.nb_lignes_visibles // 2)

        # S'assurer que les compensateurs ne dépassent pas les limites de la carte
        max_compenser_x = len(self.grid[0]) - self.nb_colonnes_visibles
        max_compenser_y = len(self.grid) - self.nb_lignes_visibles

        self.map_compenser_x = min(nouveau_compenser_x, max_compenser_x)
        self.map_compenser_y = min(nouveau_compenser_y, max_compenser_y)

        # Redessiner la carte visible
        self.dessiner_map_visible()
        print(f"Carte centrée sur le village aux coordonnées : {village_coords}, grace au compenser en x : {self.map_compenser_x}, et y : {self.map_compenser_y}")

    def dessiner_map_visible(self):
        """Redessine la portion visible de la carte en fonction du compensateur."""
        def assombrir_couleur(couleur_hex, facteur=0.7):
            """Assombrit une couleur donnée en réduisant ses composantes RGB.
            """
            # Convertir la couleur hexadécimale en RGB
            r, g, b = ImageColor.getrgb(couleur_hex)
            
            # Réduire les composantes en fonction du facteur
            r = int(r * facteur)
            g = int(g * facteur)
            b = int(b * facteur)
            
            # Retourner la couleur en format hexadécimal
            return f"#{r:02x}{g:02x}{b:02x}"
        self.canvas.delete("all")
        colors = {
            TYPE.plaine: "#eee8aa",       # palegoldenrod
            TYPE.montagne: "#808080",     # gray
            TYPE.montagneclair: "#d3d3d3",# lightgray
            TYPE.eau: "#4682b4",          # steelblue
            TYPE.eauclair: "#87ceeb",     # lightskyblue
            TYPE.foret: "#006400",        # darkgreen
            TYPE.foretclair: "#228b22",   # forestgreen
            TYPE.village: "#A67B5B"       # brown #a52a2a
        }

        colors_batiments = {
            "terrain": "#A67B5B",
            "habitation": "#C19A6B",
            "camp": "#B22222"
        }
        
        for row in range(self.nb_lignes_visibles):  # Dynamique pour les lignes
            for col in range(self.nb_colonnes_visibles):  # Dynamique pour les colonnes
                map_x = self.map_compenser_x + col
                map_y = self.map_compenser_y + row
                if 0 <= map_x < len(self.grid[0]) and 0 <= map_y < len(self.grid):
                    case = self.grid[map_y][map_x]
                    x0, y0 = col * self.case_size, row * self.case_size
                    x1, y1 = x0 + self.case_size, y0 + self.case_size
                    if case.batiment!=None:
                        color_batiment = colors_batiments.get(case.batiment, "white")
                    color = colors.get(case.type, "white")
                    # Appliquer une couleur spécifique si la case est en bordure
                    if map_x == 0 or map_y == 0 or map_x == len(self.grid[0]) - 1 or map_y == len(self.grid) - 1:
                        color = assombrir_couleur(color)
                        if case.batiment!=None:
                            color_batiment = assombrir_couleur(color_batiment)
                    elif map_x == 1 or map_y == 1 or map_x == len(self.grid[0]) - 2 or map_y == len(self.grid) - 2:
                        color = assombrir_couleur(color,.9)
                        if case.batiment!=None:
                            color_batiment = assombrir_couleur(color_batiment,.9)
                    """else:
                        if case.batiment!=None:
                            color = colors_batiments.get(case.batiment, "white")
                            print(color)
                        else:
                            color = colors.get(case.type, "white")"""
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
                    if case.batiment!=None:
                        self.canvas.create_rectangle(x0+(self.case_size/6), y0+(self.case_size/6), x1-(self.case_size/6), y1-(self.case_size/6), fill=color_batiment, outline="")
                    self.dessiner_bordures(case, x0, y0, x1, y1)
        #self.mettre_a_jour_bordures()
        keys_list = list(self.highlighted_cases.keys())
        self.highlighted_cases.clear()
        for i in keys_list:
            self.highlight_case(i[0], i[1])


    def on_click(self, event):
        """Gère les clics sur la carte."""
        from src.controllers import GameController
        from src.models import Noble, Seigneur
        # Vérifier si une action est sélectionnée
        if not self.selected_action:
            self.interface.ajouter_evenement("Aucune action sélectionnée")
            return
        
        # Calculer les coordonnées de la case cliquée
        row = event.y // self.case_size + self.map_compenser_y
        col = event.x // self.case_size + self.map_compenser_x
        case_instance = self.grid[row][col] # Récupère l'objet Case associé
        if case_instance is None:
            print("Case non trouvée.")
            return
        action_necessitant_village = ["impot", "paysan", "roturier", "immigration"]
        action_necessitant_territoire = ["acheter_case"]
        action_construire = ["terrain", "habitation", "camp"]

        # Vérifier si la caseule est un village
        village = case_instance.village
        type_case = case_instance.type
        if self.selected_action in action_necessitant_village:
            if village not in self.gamecontroller.obtenir_villages_joueur(self.gamecontroller.joueur):
                if village :
                    self.interface.ajouter_evenement("Vous ne possedez pas ce village.")
                else:
                    self.interface.ajouter_evenement("Ceci n'est pas un village.")
                return
            if village in self.selected_villages:
                self.selected_villages.remove(village)
                self.unhighlight_case(case_instance.row, case_instance.col)
                print(f"Village désélectionné : {village.nom}")
            else:
                self.selected_villages.append(village)
                self.highlight_case(case_instance.row, case_instance.col)
                print(f"Village sélectionné : {village.nom}")
        elif self.selected_action in action_construire:
            if self.selected_action == "terrain":
                if case_instance.proprietaire != None and case_instance.proprietaire != self.gamecontroller.joueur:
                    self.interface.ajouter_evenement("Ce territoire est déjà possédé par un autre joueur.")
                    return
                if case_instance.proprietaire == self.gamecontroller.joueur:
                    self.interface.ajouter_evenement("Vous possédez déjà ce territoire.")
                    return
                if not self.gamecontroller.joueur.possede_case_adjacente(case_instance):
                    self.interface.ajouter_evenement("Vous devez posséder une case adjacente.")
                    return
                """if case_instance not in self.territoire_selectionne and len(self.territoire_selectionne)==1:
                    self.unhighlight_case(self.territoire_selectionne[0].row, self.territoire_selectionne[0].col)
                    self.territoire_selectionne = []
                    self.territoire_selectionne.append(case_instance)
                    self.highlight_case(case_instance.row, case_instance.col)"""
                if case_instance not in self.territoire_selectionne:
                    self.territoire_selectionne.append(case_instance)
                    self.highlight_case(case_instance.row, case_instance.col)
                    print(f"Case sélectionnée : ({case_instance.row}, {case_instance.col})")
                elif case_instance in self.territoire_selectionne:
                    self.territoire_selectionne.remove(case_instance)
                    self.unhighlight_case(case_instance.row, case_instance.col)
                    print(f"Case désélectionnée : ({case_instance.row}, {case_instance.col})")
                else:
                    self.territoire_selectionne.remove(case_instance)
                    self.unhighlight_case(case_instance.row, case_instance.col)
                    print(f"Case désélectionnée : ({case_instance.row}, {case_instance.col})")
            elif (self.selected_action == "habitation"  or self.selected_action == "camp"):
                if case_instance.proprietaire != self.gamecontroller.joueur:
                    self.interface.ajouter_evenement("Vous ne possedez pas ce territoire.")
                    return
                elif case_instance.type != TYPE.plaine:
                    self.interface.ajouter_evenement("Vous ne pouvez pas construire ici.")
                    return
                elif case_instance.batiment:
                    self.interface.ajouter_evenement("Un batiment est déjà présent ici.")
                    return
                if case_instance not in self.territoire_selectionne and len(self.territoire_selectionne)==1:
                    self.unhighlight_case(self.territoire_selectionne[0].row, self.territoire_selectionne[0].col)
                    self.territoire_selectionne = []
                    self.territoire_selectionne.append(case_instance)
                    self.highlight_case(case_instance.row, case_instance.col)
                elif case_instance not in self.territoire_selectionne:
                    self.territoire_selectionne.append(case_instance)
                    self.highlight_case(case_instance.row, case_instance.col)
                    print(f"Case sélectionnée : ({case_instance.row}, {case_instance.col})")
                elif case_instance in self.territoire_selectionne:
                    self.territoire_selectionne.remove(case_instance)
                    self.unhighlight_case(case_instance.row, case_instance.col)
                    print(f"Case désélectionnée : ({case_instance.row}, {case_instance.col})")
                else:
                    self.territoire_selectionne.remove(case_instance)
                    self.unhighlight_case(case_instance.row, case_instance.col)
                    print(f"Case désélectionnée : ({case_instance.row}, {case_instance.col})")
        elif self.selected_action == "guerre":
            if type_case != TYPE.village:
                self.interface.ajouter_evenement("Ce n'est pas un village.")
                return
            if case_instance.village in self.gamecontroller.obtenir_villages_joueur(self.gamecontroller.joueur):
                self.interface.ajouter_evenement("Vous ne pouvez pas déclarer la guerre à votre propre village.")
                return
            if not self.territoires_adjacents(self.gamecontroller.joueur, case_instance.proprietaire):
                self.interface.ajouter_evenement("Vous devez être adjacent au territoire ennemi pour déclarer la guerre.")
                return
            if self.selected_action not in self.selected_villages and len(self.selected_villages)==1:
                self.unhighlight_case(self.selected_villages[0].row, self.selected_villages[0].col)
                self.selected_villages = []
                self.selected_villages.append(case_instance)
                self.highlight_case(case_instance.row, case_instance.col)
            elif case_instance not in self.selected_villages :
                print(case_instance)
                print(self.gamecontroller.obtenir_villages_joueur(self.gamecontroller.joueur))
                self.selected_villages.append(case_instance)
                self.highlight_case(case_instance.row, case_instance.col)
            else:
                self.selected_villages.remove(case_instance)
                self.unhighlight_case(case_instance.row, case_instance.col)
                
                print("Vous ne pouvez pas déclarer la guerre")
    
    def highlight_case(self, row, col):
        """Met en surbrillance une case sélectionnée."""
        if (row, col) in self.highlighted_cases:
            # Si déjà en surbrillance, ne rien faire
            return

        x1 = (row- self.map_compenser_x) * self.case_size
        y1 = (col- self.map_compenser_y) * self.case_size
        x2 = x1 + self.case_size
        y2 = y1 + self.case_size
        # Créer un rectangle rouge autour de la caseule
        rect_id = self.canvas.create_rectangle(
            x1, y1, x2, y2, outline="red", width=3, state="disabled"
        )
        self.highlighted_cases[(row, col)] = rect_id  # Stocker l'identifiant

    def unhighlight_case(self, row, col):
        """Réinitialise une case désélectionnée."""
        """x1 = col * self.case_size
        y1 = row * self.case_size
        x2 = x1 + self.case_size
        y2 = y1 + self.case_size
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=1)"""

        if (row, col) in self.highlighted_cases:
            # Supprimer le rectangle rouge
            self.canvas.delete(self.highlighted_cases[(row, col)])
            del self.highlighted_cases[(row, col)]  # Retirer du dictionnaire

    def clic_gauche_village(self, event):
        """
        Gère le controle clic gauche sur une case pour afficher les informations du village.
        """
        # Calculer les coordonnées de la case cliquée
        row = event.y // self.case_size + self.map_compenser_y
        col = event.x // self.case_size + self.map_compenser_x

        case_instance = self.grid[row][col] # Récupère l'objet Case associé

        # Vérifier si un village est associé à la case
        if case_instance.village or case_instance.batiment == "camp":
            village =  case_instance.village
            self.interface.mettre_a_jour_infos_village(case_instance)
            self.interface.action_bouton_selectionnee = None
            self.village_affiché = case_instance


    def get_voisins(self, case):
        """Retourne les voisins (haut, bas, gauche, droite) d'une case."""
        voisins = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Haut, bas, gauche, droite
        for d_row, d_col in directions:
            voisin_row = case.row + d_row
            voisin_col = case.col + d_col
            if 0 <= voisin_row < len(self.grid) and 0 <= voisin_col < len(self.grid[0]):
                case_instance = self.grid[voisin_col][voisin_row]
                voisins.append(case_instance)
        return voisins

    def dessiner_bordures(self, case, x1, y1, x2, y2):
        """Dessine les bordures uniquement sur les arêtes adjacentes à un territoire différent."""
        if not case.proprietaire :
            return
        voisins = self.get_voisins(case)

        # Supprime d'abord les bordures existantes
        self.canvas.delete(f"border_{case.row}_{case.col}")
        # Définir un décalage pour les bordures
        offset = 2
        # Détermine la couleur du propriétaire (seigneur ou noble)
        couleur_bordure = case.proprietaire.couleur_bordure if case.proprietaire else "black"
        #print(case.proprietaire.noble.couleur_bordure)
        for voisin in voisins:
            if voisin.proprietaire != case.proprietaire:
                if voisin.col < case.col:  # Haut
                    self.canvas.create_line(x1 + offset, y1 + offset, x2 - offset, y1 + offset, fill=couleur_bordure, width=2, tags=f"border_{case.row}_{case.col}")
                elif voisin.col > case.col:  # Bas
                    self.canvas.create_line(x1 + offset, y2 - offset, x2 - offset, y2 - offset, fill=couleur_bordure, width=2, tags=f"border_{case.row}_{case.col}")
                elif voisin.row < case.row:  # Gauche
                    self.canvas.create_line(x1 + offset, y1 + offset, x1 + offset, y2 - offset, fill=couleur_bordure, width=2, tags=f"border_{case.row}_{case.col}")
                elif voisin.row > case.row:  # Droite
                    self.canvas.create_line(x2 - offset, y1 + offset, x2 - offset, y2 - offset, fill=couleur_bordure, width=2, tags=f"border_{case.row}_{case.col}")
   
    def mettre_a_jour_bordures(self):
        """Met à jour les bordures de toutes les cases."""
        for i in self.grid:
            for case in i:
                x1, y1, x2, y2 = self.get_coords_case(case)
                self.dessiner_bordures(case, x1, y1, x2, y2)

    def get_coords_case(self, case):
        """Retourne les coordonnées de la case donnée."""
        x1 = (case.row- self.map_compenser_x) * self.case_size
        y1 = (case.col- self.map_compenser_y) * self.case_size
        x2 = x1 + self.case_size
        y2 = y1 + self.case_size
        return x1, y1, x2, y2
   
    def territoires_adjacents(self, attaquant, defenseur):
        """
        Vérifie si le territoire d'attaquant est adjacent à celui de défenseur.
        """
        for case in attaquant.cases:
            for voisin in self.get_voisins(case):
                if voisin.proprietaire == defenseur:
                    return True
        return False
    
    def chemin_le_plus_court(self,attaquant,defenseur):
        #renvoie le chemin le plus court entre 2 cases de villages differents
        """
        Trouve le chemin le plus court entre deux cases appartenant à des villages différents.
        :param attaquant: Coordonnées de la case du village attaquant (row, col).
        :param defenseur: Coordonnées de la case du village défenseur (row, col).
        :return: Liste des coordonnées représentant le chemin le plus court.
        """
        start = attaquant
        goal = defenseur

        # File pour la recherche en largeur
        queue = deque([(start, [start])])  # (case actuelle, chemin jusqu'à la case)
        visited = set()  # Ensemble des cases déjà visitées

        while queue:
            current, path = queue.popleft()

            if current in visited:
                continue

            visited.add(current)

            # Si la case actuelle est la cible, renvoyer le chemin
            if current == goal:
                #mettre toutes les cases de path en rouge
                return path

            # Ajouter les cases adjacentes à la file
            for voisin in self.get_voisins(current):
                if voisin not in visited:
                    queue.append((voisin, path + [voisin]))

        # Si aucun chemin n'est trouvé
        return []

    def to_dict(self):
        return {
            "width":self.width_map,
            "height":self.height_map,
            "cases": [[case.to_dict() for case in ligne] for ligne in self.grid]  # Assurez-vous que chaque case a une méthode to_dict()
        }