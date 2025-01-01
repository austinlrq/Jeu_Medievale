import tkinter as tk
from tkinter import font, filedialog
from tkinter import ttk
from PIL import Image, ImageTk
from ..views.interface import JeuInterface
from ..views.settingsinterface import SettingsInterface
import json
# from src.models import *
from src.models.personnes.noble import Noble
from src.models.personnes.paysan import Paysan
from src.models.personnes.roturier import Roturier
from src.models.personnes.soldat import Soldat
from src.models.fief.village import Village

from .TYPE import TYPE
from src.views.Case import Case

class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.cree_menu()

    def cree_menu(self):
        self.root.title("Menu Principal")
        self.root.geometry("540x530")
        self.root.minsize(540, 530)
        #self.root.maxsize(540, 530)
        try:
            self.root.iconbitmap("images/81709.ico")
        except tk.TclError:
            print("Icon file not found or unsupported format. Skipping icon setting.")
        self.root.configure(bg="#2E2E2E")
        self.root.resizable(True, True)

        # Cadre du menu principal
        self.menu_frame = tk.Frame(self.root, bg="#2E2E2E")
        self.menu_frame.pack(fill="both", expand=True)

        # Image de fond
        """ img = Image.open("images/image.webp")
        img = img.resize((520, 520))
        img = ImageTk.PhotoImage(img)
        self.background_label = tk.Label(self.menu_frame, image=img)
        self.background_label.image = img
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)"""

        title_font = font.Font(family="Helvetica", size=30, weight="bold")
        self.label = tk.Label(self.menu_frame, text="La Guerre des Frontières", font=title_font, bg="#2E2E2E", fg="#F7F7F7")
        self.label.place(relx=0.5, rely=0.12, anchor="center")

        separateur = ttk.Separator(self.menu_frame, orient="horizontal")
        separateur.place(relx=0.5, rely=0.25, anchor="center", relwidth=0.7)

        # Bouton pour lancer le jeu
        self.start_button = tk.Button(
            self.menu_frame,
            text="Lancer le jeu",
            font=("Helvetica", 16, "bold"),
            bg="#1C6E8C",
            fg="white",
            activebackground="#145374",
            activeforeground="white",
            command=self.lancer_jeu,
            bd=0,
            padx=20,
            pady=10
        )
        self.start_button.place(relx=0.5, rely=0.4, anchor="center")

        self.charger_button = tk.Button(
            self.menu_frame,
            text="Charger une partie",
            font=("Helvetica", 16, "bold"),
            bg="#1C6E8C",
            fg="white",
            activebackground="#145374",
            activeforeground="white",
            command=self.charger_partie,
            bd=0,
            padx=20,
            pady=10
        )
        self.charger_button.place(relx=0.5, rely=0.55, anchor="center")

        # Bouton pour lancer les settings
        self.set_button = tk.Button(
            self.menu_frame,
            text="Paramètres",
            font=("Helvetica", 16, "bold"),
            bg="#1C6E8C",
            fg="white",
            activebackground="#145374",
            activeforeground="white",
            command=self.ouvrir_settings,
            bd=0,
            padx=20,
            pady=10
        )
        self.set_button.place(relx=0.5, rely=0.7, anchor="center")

        # Bouton pour quitter
        self.quit_button = tk.Button(
            self.menu_frame,
            text="Quitter",
            font=("Helvetica", 16, "bold"),
            bg="#D9455F",
            fg="white",
            activebackground="#A63D4F",
            activeforeground="white",
            command=self.quit_game,
            bd=0,
            padx=20,
            pady=10
        )
        self.quit_button.place(relx=0.5, rely=0.85, anchor="center")
        
        self.aide_bouton = tk.Button(
            self.menu_frame,
            text="Aide",
            font=("Helvetica", 16, "bold"),
            bg="#2E2E2E",
            fg="white",
            activebackground="#2E2E2E",
            activeforeground="white",
            command=self.ouvrir_aide,
            bd=0,
            padx=20,
            pady=10,
            width=10,
            height=2
        )
        self.aide_bouton.place(relx=0.77, rely=0.89)
        
    def ouvrir_aide(self):
        from src.views import AideInterface
        AideInterface = AideInterface(self.root, self.menu_frame)
        AideInterface.afficher()

    def ouvrir_settings(self):
        """Lance l'interface des settings dans la même fenêtre."""
        self.settings = SettingsInterface(self.root, self.menu_frame)
        self.settings.creer_visu(False)  # Crée l'interface des paramètres

    def lancer_jeu(self):
        """Lance l'interface de jeu dans la même fenêtre."""
        self.menu_frame.pack_forget()  # Cache le menu principal
        self.root.minsize(900,600)
        self.root.maxsize(11520, 11520)
        self.game_frame = tk.Frame(self.root, bg="#2E2E2E")
        self.game_frame.pack(fill="both", expand=True)
        from ..controllers import GameController

        game_controller = GameController()
        JeuInterface(self.root, self.game_frame, game_controller)  # Affiche l'interface du jeu

    def charger_partie(self):
        fichier = filedialog.askopenfilename(filetypes=[("Fichiers JSON", "*.json")])
        if not fichier:
            # Si l'utilisateur clique sur "Annuler", retourner sans faire d'autres actions
            return
        if fichier:
            with open(fichier, "r") as f:
                try:
                    # Charger les données du fichier JSON
                    data = json.load(f)
                    
                    # Mettre à jour l'état du jeu avec les données chargées
                    villages, nobles, joueur = self.charger_villages(data['villages'], data['joueur'])
                    map_data = self.charger_map(data['map'], villages, nobles)
                    tour = data["tour"]
                    
                    print("Partie chargée avec succès.")
                except json.JSONDecodeError:
                    print("Erreur lors de la lecture du fichier JSON.")
        self.menu_frame.pack_forget()  # Cache le menu principal
        self.root.minsize(900,600)
        self.root.maxsize(11520, 11520)
        self.game_frame = tk.Frame(self.root, bg="#2E2E2E")
        self.game_frame.pack(fill="both", expand=True)
        from ..controllers import GameController

        game_controller = GameController(villages=villages, nobles=nobles, tour=tour, joueur = joueur)
        JeuInterface(self.root, self.game_frame, game_controller, map_data = map_data)  # Affiche l'interface du jeu

    def charger_villages(self, villages_data, joueur_data):
        villages = []
        nobles = []

        ### gerer le cas ou c'est un Seigneur ###
        
        joueur = Noble(
            joueur_data["nom"], 
            joueur_data["age"], 
            joueur_data["ressources"], 
            joueur_data["argent"], 
            joueur_data["bonheur"], 
            joueur_data["couleur_bordure"]
        )
        for village_data in villages_data:
            # Créer le village
            village = Village(village_data["id"], village_data["nom"])

            # Créer et ajouter le noble
            noble_data = village_data["noble"]
            if noble_data["nom"] == joueur.nom:
                noble = joueur
            else :
                noble = Noble(
                    noble_data["nom"], 
                    noble_data["age"], 
                    noble_data["ressources"], 
                    noble_data["argent"], 
                    noble_data["bonheur"], 
                    noble_data["couleur_bordure"]
                )
            if noble_data["armee"] != None:
                for soldat in noble_data["armee"]:
                    s = Soldat(soldat["nom"], soldat["force"], soldat["type_soldat"])
                    noble.armee.append(s)

            noble.ajouter_village(village)
            village.ajouter_noble(noble)

            # Ajouter les habitants
            for habitant_data in village_data["habitant"]:
                habitant = Roturier(
                    habitant_data["nom"], 
                    habitant_data["age"], 
                    habitant_data["ressources"], 
                    habitant_data["argent"], 
                    habitant_data["capacite_production"], 
                    habitant_data["bonheur"]
                )
                village.ajouter_habitant(habitant)

            # Ajouter le village à la liste
            villages.append(village)
            nobles.append(noble)
            print(f"{village_data['nom']} a été chargé avec succès.")
        return villages, nobles, joueur

    def charger_map(self, map_data, villages, nobles):
        # Associer chaque village avec son noble
        village_dict = {village.id: village for village in villages}
        noble_dict = {noble.nom: noble for noble in nobles}
        width = map_data['width']
        height = map_data['height']

        # Assurez-vous que la carte est correctement initialisée avec les bonnes dimensions
        grid = [[None for _ in range(width)] for _ in range(height)]
        
        # Charger les cases de la carte
        for row, cases_data in enumerate(map_data['cases']):
            for col , case_data  in enumerate(cases_data):
                print("case data",case_data, "col: ", col)
                
                # Créer la case si elle n'existe pas déjà
                if grid[row][col] is None:
                    terrain_type = self.determine_terrain_by_data(case_data)
                    grid[row][col] = Case(col, row, terrain_type)
                
                # Vérifier si cette case est un village
                if case_data["type"] == "village":
                    village = village_dict.get(case_data["village"])
                    if village:
                        case = grid[row][col]
                        case.village = village
                        village.x = col
                        village.y = row
                        # Ajouter le noble à la case
                        village.noble.ajouter_case(case)
                        print(f"Village {village.nom} placé à la position ({row}, {col}).")

                if case_data["proprietaire"] != None:
                    noble = noble_dict.get(case_data["proprietaire"])
                    if noble:
                        case = grid[row][col]
                        case.proprietaire = noble
                        noble.ajouter_case(case)

                if case_data["batiment"] != None: 
                    case = grid[row][col]
                    case.batiment = case_data["batiment"]

        return {"grid" : grid, "width": width, "height": height}
            

    def determine_terrain_by_data(self, case_data):
        # Fonction pour déterminer le terrain basé sur les données de la case JSON
        print(case_data["type"])
        if case_data["type"] == "village":
            return TYPE.village
        elif case_data["type"] == "eau":
            return TYPE.eau
        elif case_data["type"] == "foret":
            return TYPE.foret
        elif case_data["type"] == "montagne":
            return TYPE.montagne
        elif case_data["type"] == "foretclair":
            return TYPE.foretclair
        elif case_data["type"] == "eauclair":
            return TYPE.eauclair
        elif case_data["type"] == "montagneclair":
            return TYPE.montagneclair
        
        # Si le type n'est pas reconnu, renvoie la plaine par défaut
        return TYPE.plaine

    def quit_game(self):
        """Ferme le jeu."""
        self.root.quit()
