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
        
    def quitter(self):
        """Retour au menu principal."""
        self.settings_frame.place_forget()
        self.frame.pack(fill="both", expand=True)

    def creer_visu(self, en_jeu):
        """Création des éléments visuels pour l'interface des paramètres."""
        # Cache l'ancien frame
        self.frame.pack_forget()

        # Création d'un nouveau frame
        self.settings_frame = tk.Frame(self.root, bg="#2E2E2E")
        self.settings_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.lire_fichier()
        
        # Ajouter le bouton "Retour"
        self.bouton_quitter = tk.Button(
            self.settings_frame, 
            text="<  Retour", 
            command=self.quitter, 
            font=("Helvetica", 16, "bold"),
            bg="#2E2E2E",
            fg="white",
            activebackground="#2E2E2E",
            activeforeground="white",
            bd=0,
            padx=10,
            pady=5
        )
        self.bouton_quitter.pack(side="top", anchor="nw")

        # Titre
        title_label = tk.Label(self.settings_frame, text="Paramètres", font=("Helvetica", 20, "bold"), bg="#2E2E2E", fg="#F7F7F7")
        title_label.place(relx=0.5, rely=0.1, anchor="center")

        # Sensibilité
        label_sensi = tk.Label(self.settings_frame, text="Sensibilité :", font=self.title_font, bg="#2E2E2E", fg="#F7F7F7")
        label_sensi.place(relx=0.4, rely=0.2, anchor="e")
        self.sensibilite_range = tk.Scale(self.settings_frame, from_=1, to=10, orient=tk.HORIZONTAL, bg="#2E2E2E", fg="#F7F7F7",
                                          highlightthickness=0, troughcolor="#1C1C1C")
        self.sensibilite_range.set(self.sensibilite)
        self.sensibilite_range.place(relx=0.45, rely=0.2, anchor="w")

        # Hauteur de la carte
        label_hauteur_map = tk.Label(self.settings_frame, text="Hauteur de la carte :", font=self.title_font, bg="#2E2E2E", fg="#F7F7F7")
        label_hauteur_map.place(relx=0.4, rely=0.3, anchor="e")
        self.hauteur_map_var = tk.IntVar(value=self.hauteur_map)
        hauteur_map_menu = tk.OptionMenu(self.settings_frame, self.hauteur_map_var, 25, 50, 75, 100)
        hauteur_map_menu.config(font=("Helvetica", 14), bg="#2E2E2E", fg="#F7F7F7", highlightthickness=0)
        hauteur_map_menu.place(relx=0.45, rely=0.3, anchor="w")

        # Largeur de la carte
        label_largeur_map = tk.Label(self.settings_frame, text="Largeur de la carte :", font=self.title_font, bg="#2E2E2E", fg="#F7F7F7")
        label_largeur_map.place(relx=0.4, rely=0.4, anchor="e")
        self.largeur_map_var = tk.IntVar(value=self.largeur_map)
        largeur_map_menu = tk.OptionMenu(self.settings_frame, self.largeur_map_var, 25, 50, 75, 100)
        largeur_map_menu.config(font=("Helvetica", 14), bg="#2E2E2E", fg="#F7F7F7", highlightthickness=0)
        largeur_map_menu.place(relx=0.45, rely=0.4, anchor="w")

        # Nombre de villages
        label_villages = tk.Label(self.settings_frame, text="Nombre de villages :", font=self.title_font, bg="#2E2E2E", fg="#F7F7F7")
        label_villages.place(relx=0.4, rely=0.5, anchor="e")
        self.villages_range = tk.Scale(self.settings_frame, from_=1, to=6, orient=tk.HORIZONTAL, bg="#2E2E2E", fg="#F7F7F7",
                                       highlightthickness=0, troughcolor="#1C1C1C")
        self.villages_range.set(self.nb_village)
        self.villages_range.place(relx=0.45, rely=0.5, anchor="w")

        # Seed
        label_seed = tk.Label(self.settings_frame, text="Seed :", font=self.title_font, bg="#2E2E2E", fg="#F7F7F7")
        label_seed.place(relx=0.4, rely=0.6, anchor="e")
        self.seed_entry = tk.Entry(self.settings_frame, font=("Helvetica", 14), bg="#F7F7F7", fg="#2E2E2E")
        self.seed_entry.insert(0, str(self.seed))
        self.seed_entry.place(relx=0.45, rely=0.6, anchor="w", width=200)
        
        if en_jeu:
            hauteur_map_menu.config(state="disabled")
            label_hauteur_map.config(fg="gray")

            largeur_map_menu.config(state="disabled")
            label_largeur_map.config(fg="gray")

            self.villages_range.config(state="disabled")
            label_villages.config(fg="gray")

            self.seed_entry.config(state="disabled")
            label_seed.config(fg="gray")

        # Bouton pour sauvegarder
        save_button = tk.Button(self.settings_frame, text="Sauvegarder", font=("Helvetica", 16, "bold"), command=self.sauver, bg="#1C6E8C", fg="white", activebackground="#145374",activeforeground="white", relief="flat")
        save_button.place(relx=0.5, rely=0.8, anchor="center", width=150, height=50)

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

        # Revenir au menu principal
        self.settings_frame.place_forget()
        self.frame.pack(fill="both", expand=True)
