import tkinter as tk
from tkinter import font
from ..controllers import GameController
from ..views.generationmap import Map
from ..views.interface import JeuInterface

class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu Médiéval - Menu Principal")
        self.root.geometry("400x300")
        self.root.configure(bg="#2E2E2E")
        self.root.resizable(False, False)

        # Cadre du menu principal
        self.menu_frame = tk.Frame(root, bg="#2E2E2E")
        self.menu_frame.pack(fill="both", expand=True)

        title_font = font.Font(family="Helvetica", size=36, weight="bold")
        self.label = tk.Label(self.menu_frame, text="Jeu Médiéval", font=title_font, bg="#2E2E2E", fg="#F7F7F7")
        self.label.pack(pady=30)

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
        self.start_button.pack(pady=20)

        # Bouton pour quitter
        self.quit_button = tk.Button(
            self.menu_frame,
            text="Quitter",
            font=("Helvetica", 16, "bold"),
            bg="#D9455F",
            fg="white",
            activebackground="#A63D4F",
            activeforeground="white",
            command=root.quit,
            bd=0,
            padx=20,
            pady=10
        )
        self.quit_button.pack(pady=10)

    def lancer_jeu(self):
        """Lance l'interface de jeu dans la même fenêtre."""
        self.menu_frame.pack_forget()  # Cache le menu principal
        self.game_frame = tk.Frame(self.root, bg="#2E2E2E")
        self.game_frame.pack(fill="both", expand=True)
        game_controller=GameController(1)
        map = Map(20,20,game_controller.liste_joueurs,15153)
        # map.show_map(50)
        print(game_controller.joueur.argent)
        JeuInterface(self.root, self.game_frame, game_controller, map)  # Affiche l'interface du jeu