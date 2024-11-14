import tkinter as tk
from tkinter import font
from ..views.generationmap import Map
from ..views.Type import TYPE
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

        # Cadre pour la carte (grille)
        self.map_frame = tk.Frame(self.main_frame, bg="#2E2E2E")
        self.map_frame.pack(expand=True, fill="both", padx=20, pady=10)
        self.map = map
        self.map_offset_x = 0  # Horizontal map offset
        self.map_offset_y = 0  # Vertical map offset
        self.start_x = 0       # Initial x position for dragging
        self.start_y = 0       # Initial y position for dragging

        # Create map and bind mouse events for dragging
        self.creer_grille_carte(50)
        self.canvas.bind("<ButtonPress-1>", self.on_map_click)
        self.canvas.bind("<B1-Motion>", self.on_map_drag)
        
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

    def creer_grille_carte(self, cell_size):
        self.cell_size = cell_size
        self.canvas = tk.Canvas(self.map_frame, width=12 * cell_size, height=8 * cell_size, bg="#2E2E2E", highlightthickness=0)
        self.canvas.pack(anchor="center")

        self.draw_visible_map()

    def draw_visible_map(self):
        """Redraws the visible portion of the map based on the offset."""
        self.canvas.delete("all")
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
        
        for row in range(8):  # Display 8 rows
            for col in range(12):  # Display 12 columns
                map_x = self.map_offset_x + col
                map_y = self.map_offset_y + row
                if 0 <= map_x < len(self.map.grid[0]) and 0 <= map_y < len(self.map.grid):
                    cell = self.map.grid[map_y][map_x]
                    x0, y0 = col * self.cell_size, row * self.cell_size
                    x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                    color = colors.get(cell.type, "white")
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

                    # Add ownership pattern if applicable
                    if cell.proprio and cell.type != TYPE.village:
                        for k in range(0, self.cell_size + 1, 10):
                            self.canvas.create_line(x0 + k, y0, x0, y0 + k, fill=cell.proprio.couleur, width=1)
                            self.canvas.create_line(x1 - k, y1, x1, y1 - k, fill=cell.proprio.couleur, width=1)

    def on_map_click(self, event):
        """Handles the start of a drag by storing the initial click position."""
        self.start_x = event.x
        self.start_y = event.y

    def on_map_drag(self, event):
        """Handles map dragging to update the offset and redraw the visible map."""
        sensibilite = 5
        dx = int(int(event.x - self.start_x) / sensibilite)
        dy = int(int(event.y - self.start_y )/ sensibilite)

        print(dx)

        # Update offsets
        new_offset_x = self.map_offset_x - dx
        new_offset_y = self.map_offset_y - dy

        # Boundaries check: Prevent scrolling beyond map limits
        max_offset_x = len(self.map.grid[0]) - 12
        max_offset_y = len(self.map.grid) - 8

        # Ensure the offsets are within valid bounds
        new_offset_x = max(min(new_offset_x, max_offset_x), 0)
        new_offset_y = max(min(new_offset_y, max_offset_y), 0)

        if new_offset_x != self.map_offset_x or new_offset_y != self.map_offset_y:
            self.map_offset_x, self.map_offset_y = new_offset_x, new_offset_y
            self.draw_visible_map()

        # Update start position for smoother drag
        self.start_x, self.start_y = event.x, event.y


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
        print(self.gamecontroller.village_joueur.afficher_statut())
    
    def executer_action_selectionnee(self):
        #print("oui")
        if self.action_selectionnee == "impot":
            
            self.gamecontroller.joueur.percevoir_impots()
            print("Action exécutée: Produire des ressources")
            self.gamecontroller.appliquer_evenements(self.gamecontroller.village_joueur.habitants)
            self.mettre_a_jour_infos()

        self.action_selectionnee = None
        self.reset_bouton_couleurs()
        self.mettre_a_jour_infos()
        print(self.gamecontroller.joueur.argent)

        