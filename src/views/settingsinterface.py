import tkinter as tk
from tkinter import font
import json

class SettingsInterface:
    def __init__(self, root, frame):
        self.root = root
        self.title_font = font.Font(family="Helvetica", size=15, weight="bold")
        self.frame = frame

    def lire_fichier(self):
        """Lecture du fichier JSON des paramètres."""
        with open("src/settings.json", "r") as f:
            data = json.load(f)
        self.hauteur_map = data["HAUTEUR_MAP"]
        self.largeur_map = data["LARGEUR_MAP"]
        self.nb_village = data["NB_VILLAGE"]
        self.sensibilite = data["SENSIBILITE"]
        self.seed = data["SEED"]

    def creer_visu(self, en_jeu):
        """Création des éléments visuels pour l'interface des paramètres avec Scrollbar et layout en grille."""
        # Cache l'ancien frame
        self.frame.pack_forget()
        self.canvas = tk.Canvas(self.root, bg="#2E2E2E", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#2E2E2E")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Affichage des widgets
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Widgets de l'interface des paramètres
        self.lire_fichier()

        # Label "Settings" en haut
        title_label = tk.Label(self.scrollable_frame, text="Settings", font=("Helvetica", 20, "bold"), bg="#2E2E2E", fg="#F7F7F7")
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Sensibilité
        self.label_sensi = tk.Label(self.scrollable_frame, text="Sensibilité :", font=self.title_font, bg="#2E2E2E", fg="#F7F7F7")
        self.label_sensi.grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.sensibilite_range = tk.Scale(self.scrollable_frame, from_=1, to=10, orient=tk.HORIZONTAL, bg="#2E2E2E", fg="#F7F7F7", 
                                        highlightthickness=0, borderwidth=0, troughcolor="#1C1C1C")
        self.sensibilite_range.set(self.sensibilite)
        self.sensibilite_range.grid(row=1, column=1, sticky="w", padx=10, pady=(0, 14))  # Déplace uniquement le Scale

        # Hauteur de la carte
        self.label_hauteur_map = tk.Label(self.scrollable_frame, text="Hauteur de la carte :", font=self.title_font, bg="#2E2E2E", fg="#F7F7F7")
        self.label_hauteur_map.grid(row=2, column=0, sticky="e", padx=10, pady=10)
        self.hauteur_map_var = tk.IntVar(value=self.hauteur_map)
        self.hauteur_map_menu = tk.OptionMenu(self.scrollable_frame, self.hauteur_map_var, 25, 50, 75, 100)
        self.hauteur_map_menu.config(font=("Helvetica", 14), bg="#2E2E2E", fg="#F7F7F7",
                                     highlightthickness=0, borderwidth=0,)
        self.hauteur_map_menu.grid(row=2, column=1, sticky="w", padx=10, pady=10) 

        # Largeur de la carte
        self.label_largeur_map = tk.Label(self.scrollable_frame, text="Largeur de la carte :", font=self.title_font, bg="#2E2E2E", fg="#F7F7F7")
        self.label_largeur_map.grid(row=3, column=0, sticky="e", padx=10, pady=10)
        self.largeur_map_var = tk.IntVar(value=self.largeur_map)
        self.largeur_map_menu = tk.OptionMenu(self.scrollable_frame, self.largeur_map_var, 25, 50, 75, 100)
        self.largeur_map_menu.config(font=("Helvetica", 14), bg="#2E2E2E", fg="#F7F7F7",
                                     highlightthickness=0, borderwidth=0,)
        self.largeur_map_menu.grid(row=3, column=1, sticky="w", padx=10, pady=10)  

        # Nombre de villages
        self.label_villages = tk.Label(self.scrollable_frame, text="Nombre de villages :", font=self.title_font, bg="#2E2E2E", fg="#F7F7F7")
        self.label_villages.grid(row=4, column=0, sticky="e", padx=10, pady=10)
        self.villages_range = tk.Scale(self.scrollable_frame, from_=1, to=6, orient=tk.HORIZONTAL, bg="#2E2E2E", fg="#F7F7F7",
                                       highlightthickness=0, borderwidth=0, troughcolor="#1C1C1C")
        self.villages_range.set(self.nb_village)
        self.villages_range.grid(row=4, column=1, sticky="w", padx=10, pady=(0, 14)) 

        # Seed (input entry)
        self.label_seed = tk.Label(self.scrollable_frame, text="Seed :", font=self.title_font, bg="#2E2E2E", fg="#F7F7F7")
        self.label_seed.grid(row=5, column=0, sticky="e", padx=10, pady=10)
        self.seed_entry = tk.Entry(self.scrollable_frame, font=("Helvetica", 14), bg="#F7F7F7", fg="#2E2E2E")
        self.seed_entry.insert(0, str(self.seed))  # Default seed value
        self.seed_entry.grid(row=5, column=1, sticky="w", padx=10, pady=10)  # Déplace uniquement le Entry

        if en_jeu:
            self.hauteur_map_menu.config(state="disabled")
            self.label_hauteur_map.config(fg="gray")

            self.largeur_map_menu.config(state="disabled")
            self.label_largeur_map.config(fg="gray")

            self.villages_range.config(state="disabled")
            self.label_villages.config(fg="gray")

            self.seed_entry.config(state="disabled")
            self.label_seed.config(fg="gray")

        # Bouton pour sauvegarder
        self.save_button = tk.Button(self.scrollable_frame, text="Sauver", font=("Helvetica", 16, "bold"), command=self.sauver, bg="#1C6E8C", fg="white")
        self.save_button.grid(row=6, column=0, columnspan=2, pady=20)

    def sauver(self):
        """Sauvegarde les paramètres modifiés dans le fichier JSON."""
        self.hauteur_map = self.hauteur_map_var.get()
        self.largeur_map = self.largeur_map_var.get()
        self.nb_village = self.villages_range.get()
        self.seed = int(self.seed_entry.get())

        data = {
            "NB_VILLAGE": self.nb_village,
            "HAUTEUR_MAP": self.hauteur_map,
            "LARGEUR_MAP": self.largeur_map,
            "SEED": self.seed,
            "SENSIBILITE": self.sensibilite_range.get()
        }

        with open("src/settings.json", "w") as f:
            json.dump(data, f)

        # Revenir au menu
        self.canvas.pack_forget()
        self.scrollbar.pack_forget()
        self.frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1.0, relheight=1.0)
