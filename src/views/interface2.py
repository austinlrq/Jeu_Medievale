import tkinter as tk
from tkinter import font
from ..views.generationmap import Map
from ..views.TYPE import TYPE
from ..models.actions.acheter_case import AcheterCase
from ..views.mapdrag import MapDrag
from ..views.mapzoom import MapZoom
from PIL import ImageColor
# from ..models import *
# from ..controllers import *

class JeuInterface:
    def __init__(self, root, main_frame, game_controller, map:Map):
        self.root = root
        self.main_frame = main_frame
        self.gamecontroller = game_controller
        self.root.title("Jeu Médiéval")
        self.root.geometry("800x600")
        self.root.configure(bg="#2E2E2E")
        self.root.resizable(True, True)
        self.action_selectionnee = None

        # Cadre pour l'affichage des informations en haut
        self.info_frame = tk.Frame(self.main_frame, height=50, bg="#3A3A3A")
        self.info_frame.pack(fill="x", pady=(10, 5))
        self.afficher_informations()

        # Initialiser la classe AcheterCase avec le jeu interface
        self.acheter_case = AcheterCase(self)
        self.mode_achat = tk.BooleanVar(value=False)  # Variable pour suivre l'état du mode achat

        # Cadre pour la carte (grille)
        self.map_frame = tk.Frame(self.main_frame, bg="#2E2E2E")
        self.map_frame.pack(expand=True, fill="both", padx=20, pady=10)
        self.map = map
        
        
        # Create map and bind mouse events for dragging
        self.creer_grille_carte(50)
        # Initialiser les gestionnaires pour zoom et drag
        self.zoom_manager = MapZoom(self.canvas, self)
        self.drag_manager = MapDrag(self.canvas, self)
        
        # Bind espace pour retrouver le village facilement
        self.root.bind("<space>", lambda event: self.centrer_sur_village())
        # Clic droit pour achat
        self.canvas.bind("<Button-1>", self.sur_map_click)  

        
        # Cadre pour les actions en bas
        self.actions_frame = tk.Frame(self.main_frame, height=50, bg="#3A3A3A")
        self.actions_frame.pack(fill="x", pady=(5, 10))
        self.afficher_actions()
        self.tour_suivant()

    def afficher_informations(self):
        label_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.argent_label = tk.Label(self.info_frame, text=f"Argent : {self.gamecontroller.joueur.argent}", bg="#3A3A3A", fg="#F7F7F7", font=label_font)
        self.argent_label.pack(side="left", padx=15)
        self.ressources_label = tk.Label(self.info_frame, text=f"Ressources : {self.gamecontroller.joueur.ressources}", bg="#3A3A3A", fg="#F7F7F7", font=label_font)
        self.ressources_label.pack(side="left", padx=15)
    
    def mettre_a_jour_infos(self):
        """Met à jour l'interface avec les infos actuelles du jeu."""
        # Accède aux informations du joueur et du village depuis `etat_du_jeu`
        self.argent_label.config(text=f"Argent : {self.gamecontroller.joueur.argent}")
        self.ressources_label.config(text=f"Ressources : {self.gamecontroller.joueur.ressources}")
        self.mettre_a_jour_boutons()

    def mettre_a_jour_boutons(self):
        """Mise à jour de l'état des boutons selon l'argent du joueur."""
        if self.gamecontroller.joueur.argent <= 0:
            self.achat_bouton.config(state="disabled", bg="#555555")
        else:
            self.achat_bouton.config(state="normal", bg="green" if self.mode_achat.get() else "#1C6E8C")


    #########
    # CARTE #
    #########
    def creer_grille_carte(self, cell_size):
        self.map_compenser_x = 0  # Compensateur horizontal de la carte
        self.map_compenser_y = 0  # Compensateur vertical de la carte
        self.debut_x = 0         # Position initiale en x pour le glissement
        self.debut_y = 0         # Position initiale en y pour le glissement
        self.cell_size = cell_size
        self.canvas = tk.Canvas(self.map_frame, width=12 * cell_size, height=8 * cell_size, bg="#2E2E2E", highlightthickness=0)
        self.canvas.pack(anchor="center")
        self.root.update_idletasks()  # Force l'actualisation de la fenêtre
        self.nb_colonnes_visibles = self.canvas.winfo_width() // self.cell_size
        self.nb_lignes_visibles = self.canvas.winfo_height() // self.cell_size

        self.centrer_sur_village()
            
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
            TYPE.village: "#a52a2a"       # brown
        }

        for row in range(self.nb_lignes_visibles):  # Dynamique pour les lignes
            for col in range(self.nb_colonnes_visibles):  # Dynamique pour les colonnes
                map_x = self.map_compenser_x + col
                map_y = self.map_compenser_y + row
                if 0 <= map_x < len(self.map.grid[0]) and 0 <= map_y < len(self.map.grid):
                    cell = self.map.grid[map_y][map_x]
                    x0, y0 = col * self.cell_size, row * self.cell_size
                    x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                    color = colors.get(cell.type, "white")
                    # Appliquer une couleur spécifique si la case est en bordure
                    if map_x == 0 or map_y == 0 or map_x == len(self.map.grid[0]) - 1 or map_y == len(self.map.grid) - 1:
                        color = assombrir_couleur(color)
                    elif map_x == 1 or map_y == 1 or map_x == len(self.map.grid[0]) - 2 or map_y == len(self.map.grid) - 2:
                        color = assombrir_couleur(color,.9)
                    else:
                        color = colors.get(cell.type, "white")
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

                    # Si le mode achat est active et la case est voisine a un des village du joueur et que ce n'est pas une case deja occupe. 
                    # Mettre la case en jaune
                    if (self.mode_achat.get() and self.acheter_case.est_voisine_village(map_x,map_y,self.gamecontroller.joueur) 
                        and cell.type != TYPE.village and cell.villageproprio is None):
                        c2 = self.cell_size // 3
                        self.canvas.create_oval(x0 + c2 , y0 + c2, x1 - c2, y1 - c2, fill='yellow', outline="")
                    # Ajouter un motif de propriété si applicable
                    if cell.villageproprio and cell.type != TYPE.village:
                        for k in range(0, self.cell_size + 1, 10):
                            self.canvas.create_line(x0 + k, y0, x0, y0 + k, fill=cell.villageproprio.couleur, width=1)
                            self.canvas.create_line(x1 - k, y1, x1, y1 - k, fill=cell.villageproprio.couleur, width=1)

    def centrer_sur_village(self):
        """Centre la carte sur le village du joueur."""
        # Récupérer les coordonnées du village du joueur
        village_coords = self.gamecontroller.joueur.coord_village()  # (x, y)
        
        if not village_coords:
            print("Aucun village trouvé pour centrer la carte.")
            return

        village_x, village_y = village_coords

        # Calculer les nouveaux compensateurs pour centrer le village
        nouveau_compenser_x = max(0, village_x - self.nb_colonnes_visibles // 2)
        nouveau_compenser_y = max(0, village_y - self.nb_lignes_visibles // 2)

        # S'assurer que les compensateurs ne dépassent pas les limites de la carte
        max_compenser_x = len(self.map.grid[0]) - self.nb_colonnes_visibles
        max_compenser_y = len(self.map.grid) - self.nb_lignes_visibles

        self.map_compenser_x = min(nouveau_compenser_x, max_compenser_x)
        self.map_compenser_y = min(nouveau_compenser_y, max_compenser_y)

        # Redessiner la carte visible
        self.dessiner_map_visible()
        print(f"Carte centrée sur le village aux coordonnées : {village_coords}, grace au compenser en x : {self.map_compenser_x}, et y : {self.map_compenser_y}")
    

    def afficher_actions(self):
        button_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.impot_bouton = tk.Button(
            self.actions_frame,
            text="Impot",
            command=lambda: self.selectionner_action("impot"),
            font=button_font,
            bg="#1C6E8C",
            fg="white",
            activebackground="#145374",
            activeforeground="white",
            bd=0,
            padx=20,
            pady=5
        )
        self.impot_bouton.pack(side="left", padx=15)

        self.achat_bouton = tk.Button(
            self.actions_frame,
            text="Mode Achat",
            command=self.activer_mode_achat,
            font=button_font,
            bg="#1C6E8C",
            fg="white",
            activebackground="#145374",
            activeforeground="white",
            bd=0,
            padx=20,
            pady=5
        )
        self.achat_bouton.pack(side="left", padx=10)

    def activer_mode_achat(self):
        """Active ou désactive le mode achat."""
        if not self.mode_achat.get():
            print("Mode achat activé")
            self.mode_achat.set(True)
            self.achat_bouton.config(bg="green")
            self.dessiner_map_visible()
        else:
            print("Mode achat désactivé")
            self.mode_achat.set(False)
            self.achat_bouton.config(bg="#1C6E8C")
            self.dessiner_map_visible()

    def sur_map_click(self, event):
        """Gère l'achat de cases via un clic gauche."""
        if not self.mode_achat.get():
            print("Mode achat désactivé. Clic ignoré.")
            return

        # Calculer la colonne et la ligne cliquées
        col = (event.x // self.cell_size) + self.map_compenser_x
        row = (event.y // self.cell_size) + self.map_compenser_y

        # Effectuer l'achat
        print(f"Achat tenté sur la case ({col}, {row})")
        self.acheter_case.acheter_case(col, row, self.gamecontroller.joueur, self.mode_achat)
        self.dessiner_map_visible()


    def selectionner_action(self,action):
        if self.action_selectionnee == action:
            self.action_selectionnee = None
            self.reset_bouton_couleurs()
        else:
            self.action_selectionnee = action
            self.reset_bouton_couleurs()
            if action == "impot":
                self.impot_bouton.config(bg="#3498DB")

    def reset_bouton_couleurs(self):
        self.impot_bouton.config(bg="#1C6E8C")

    def tour_suivant(self):
        button_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.tour_suivant_bouton = tk.Button(
            self.actions_frame,
            text="Valider/Tour Suivant",
            command=self.executer_action_selectionnee,
            font=button_font,
            bg="#1C6E8C",
            fg="white", 
            activebackground="#145374",
            activeforeground="white",
            bd=0,
            padx=20,
            pady=5
        )
        self.tour_suivant_bouton.pack(side="right", padx=15)
        print("joueur village statut: ",self.gamecontroller.joueur.villages[0].afficher_statut())
    
    def executer_action_selectionnee(self):
        #print("oui")
        if self.action_selectionnee == "impot":
            self.gamecontroller.joueur.percevoir_impots()
            print("Action exécutée: Produire des ressources")
            # self.gamecontroller.appliquer_evenements(self.gamecontroller.village_joueur.habitants)
            self.mettre_a_jour_infos()

        self.action_selectionnee = None
        self.reset_bouton_couleurs()
        self.mettre_a_jour_infos()
        print("argent joueur:" ,self.gamecontroller.joueur.argent)

        