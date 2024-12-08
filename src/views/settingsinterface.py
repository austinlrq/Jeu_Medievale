import tkinter as tk
from tkinter import font
import json

class SettingsInterface():
    def __init__(self, root, menu):
        self.menu = menu
        self.root = root
        self.root.title("Jeu Médiéval - Menu Principal")

        # Cadre 
        self.settings_frame = tk.Frame(root, bg="#2E2E2E")
        self.settings_frame.pack(fill="both", expand=True)
        
        # lecture du fichier
        with open("src/settings.json", "r") as f:
           data = json.load(f)
        taille_map = data["TAILLE_MAP"]
        nb_bot = data["NB_BOT"]
        sensibilite = data["SENSIBILITE"]
        
        title_font = font.Font(family="Helvetica", size=15, weight="bold")
        
        # SENSIBILITE
        self.label_sensi = tk.Label(self.settings_frame, text="Sensibilité", font=title_font, bg="#2E2E2E", fg="#F7F7F7")
        self.label_sensi.pack(pady=30)
        self.sensibilite_range = tk.Scale(self.settings_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        self.sensibilite_range.set(sensibilite)
        self.sensibilite_range.pack()
        
        
        # Bouton pour lancer le jeu
        self.start_button = tk.Button(
            self.settings_frame,
            text="Sauver",
            font=("Helvetica", 16, "bold"),
            bg="#1C6E8C",
            fg="white",
            activebackground="#145374",
            activeforeground="white",
            command=self.sauver,
            bd=0,
            padx=20,
            pady=10
        )
        self.start_button.pack(pady=20)
        
    def sauver(self):
        print (self.sensibilite_range.get())
        data = {
            "NB_BOT": 3,
            "TAILLE_MAP": 50,
            "SEED": 1515,
            "SENSIBILITE": self.sensibilite_range.get()
        }

        with open("src/settings.json", "w") as f:
            json.dump(data, f)
            
        self.settings_frame.pack_forget()
        self.menu.cree_menu()
        
        
        
        
        
        
        
        
        
        