import tkinter as tk
from tkinter import font, Toplevel, ttk
from ..models import *
from ..controllers import *

class JeuInterface:
    def __init__(self, root, main_frame, game_controller):
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
        self.info_frame.pack(fill="x", pady=0)
        self.afficher_informations()

        """# Cadre pour la carte (grille)
        self.map_frame = tk.Frame(self.main_frame, bg="#2E2E2E")
        self.map_frame.pack(expand=True, fill="both", padx=20, pady=10)
        from .map import Map
        self.map = Map(self.map_frame, self.gamecontroller, rows=10, cols=10, cell_size=50)"""

        # Cadre principal avec deux colonnes
        self.main_content = tk.Frame(self.main_frame, bg="#2E2E2E")
        self.main_content.pack(expand=True, fill="both", padx=10, pady=10)

        # Colonne de gauche : carte
        self.map_frame = tk.Frame(self.main_content, bg="#2E2E2E")
        self.map_frame.pack(side=tk.LEFT, expand=True, fill="both")
        from .map import Map
        self.map = Map(self.map_frame, self.gamecontroller, rows=10, cols=10, cell_size=50)
        self.map.interface = self

        # Colonne de droite : cadre principal pour les informations et le journal
        self.right_frame = tk.Frame(self.main_content, width=200, bg="#3A3A3A")
        self.right_frame.pack(side=tk.RIGHT, fill="y", padx=5)

        # Cadre pour les informations du village
        self.village_info_frame = tk.Frame(self.right_frame, bg="#2E2E2E", height=110)
        self.village_info_frame.pack_propagate(False)
        self.village_info_frame.pack(fill="x", pady=5, padx=5)

        self.village_info_label = tk.Label(
            self.village_info_frame,
            text="Clique droit sur un village pour voir ses informations",
            bg="#2E2E2E",
            fg="#F7F7F7",
            font=("Helvetica", 12),
            wraplength=180,
            justify="left",
        )
        self.village_info_label.pack(fill="both", expand=True, padx=3, pady=(0,0))

        # Zone de texte avec scrollbar pour les événements
        self.journal_text = tk.Text(self.right_frame, wrap=tk.WORD, state=tk.DISABLED, width=30, height=0, bg="#3A3A3A", fg="#F7F7F7")
        self.journal_text.pack(side=tk.LEFT, fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self.right_frame, orient=tk.VERTICAL, command=self.journal_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.journal_text.config(yscrollcommand=self.scrollbar.set)

        # Cadre pour les actions en bas
        self.actions_frame = tk.Frame(self.main_frame, height=50, bg="#3A3A3A")
        self.actions_frame.pack(fill="x", pady=0)
        self.afficher_actions()
        self.tour_suivant()

        

    def afficher_informations(self):
        label_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.argent_label = tk.Label(self.info_frame, text=f"Argent : {self.gamecontroller.joueur.argent}", bg="#3A3A3A", fg="#F7F7F7", font=label_font)
        self.argent_label.pack(side="left", padx=15)
        self.ressources_label = tk.Label(self.info_frame, text=f"Ressources : {self.gamecontroller.joueur.ressources}", bg="#3A3A3A", fg="#F7F7F7", font=label_font)
        self.ressources_label.pack(side="left", padx=15)
        self.population_label = tk.Label(self.info_frame, text=f"Nombre d'habitants : {self.gamecontroller.joueur.village_noble.population}", bg="#3A3A3A", fg="#F7F7F7", font=label_font)
        self.population_label.pack(side="left", padx=15)
        self.tour_label = tk.Label(self.info_frame, text=f"Tour : {self.gamecontroller.tour}", bg="#3A3A3A", fg="#F7F7F7", font=label_font)
        self.tour_label.pack(side="right", padx=15)
    
    def mettre_a_jour_infos(self):
        """Met à jour l'interface avec les infos actuelles du jeu."""
        # Accède aux informations du joueur et du village depuis `etat_du_jeu`
        self.argent_label.config(text=f"Argent : {self.gamecontroller.joueur.argent}")
        self.ressources_label.config(text=f"Ressources : {self.gamecontroller.joueur.ressources}")
        self.population_label.config(text=f"Nombre d'habitants : {self.gamecontroller.joueur.village_noble.population}")
        self.tour_label.config(text=f"Tour : {self.gamecontroller.tour}")

    def ajouter_evenement(self, texte):
        """
        Ajoute un événement au journal des événements.
        """
        self.journal_text.config(state=tk.NORMAL)  # Débloquer le widget pour écrire
        self.journal_text.insert(tk.END, texte + "\n")  # Ajouter à la fin
        self.journal_text.see(tk.END)  # Scroller automatiquement vers le bas
        self.journal_text.config(state=tk.DISABLED)  # Rebloquer le widget

    def mettre_a_jour_infos_village(self, village):
        """
        Met à jour les informations affichées sur le village sélectionné.
        """
        if village:
            infos = (
                f"              {village.nom}\n\n"
                f"Population : {village.population}\n"
                f"Ressources habitants : {village.total_ressources}\n"
                f"Argent habitants : {village.total_argent}"
                #f"Seigneur : {village.seigneur.nom if village.seigneur else 'Aucun'}"
            )
        else:
            infos = "Aucun village sélectionné."

        self.village_info_label.config(text=infos)


    def afficher_actions(self):
        button_font = font.Font(family="Helvetica", size=12, weight="bold")

        # Bouton Impôt
        self.impot_bouton = tk.Button(
            self.actions_frame,
            text="Impôt",
            command=lambda: self.selectionner_action("impot"),
            font=button_font,
            bg="#1C6E8C",
            fg="white",
            activebackground="#145374",
            activeforeground="white",
            bd=0,
            padx=10,
            pady=5,
            height=1,
            width=8,
            anchor="center"  # Centrer le texte
        )
        self.impot_bouton.pack(side="left", padx=10, pady=5)

        # Bouton Immigration avec un menu déroulant stylisé
        self.immigration_bouton = tk.Menubutton(
            self.actions_frame,
            text="Immigration",
            font=button_font,
            bg="#1C6E8C",
            fg="white",
            activebackground="#145374",
            activeforeground="white",
            bd=0,
            padx=10,
            pady=5,
            #relief="flat",
            height=1,
            width=8,
            anchor="center"  # Centrer le texte
        )
        self.immigration_bouton.pack(side="left", padx=10, pady=5)

        # Ajouter le menu déroulant
        self.immigration_menu = tk.Menu(
            self.immigration_bouton,
            tearoff=0,
            bg="#3A3A3A",
            fg="#F7F7F7",
            activebackground="#145374",
            activeforeground="white",
            font=("Helvetica", 10)
        )
        self.immigration_bouton.configure(menu=self.immigration_menu)

        # Ajouter les options au menu déroulant
        self.immigration_menu.add_command(label="Paysan", command=lambda: self.selectionner_action("paysan"))
        self.immigration_menu.add_command(label="Roturier", command=lambda: self.selectionner_action("roturier"))

    
    
    def selectionner_action(self, action):
        if self.action_selectionnee == action:
            self.action_selectionnee = None
            self.map.selected_action = None  # Réinitialiser l'action sur la carte
            self.reset_bouton_couleurs()
        else:
            self.action_selectionnee = action
            self.map.selected_action = action  # Définir l'action sélectionnée
            self.reset_bouton_couleurs()
            if action == "impot":
                self.impot_bouton.config(bg="#3498DB")
            elif action == "immigration":
                self.immigration_bouton.config(bg="#3498DB")
            elif action == "paysan" or action == "roturier":
                self.immigration_bouton.config(bg="#3498DB")
        liste = []
        for i in self.map.highlighted_cells:
            liste.append(i)
        for j in liste:
            self.map.unhighlight_cell(j[0],j[1])
        self.map.selected_villages = []

    def reset_bouton_couleurs(self):
        self.impot_bouton.config(bg="#1C6E8C")
        self.immigration_bouton.config(bg="#1C6E8C")

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
    
    def executer_action_selectionnee(self):
        from src.models import Immigration
        if self.action_selectionnee != None:
            if self.action_selectionnee == "impot" and self.map.selected_villages != []:
                impot = 0
                for i in self.map.selected_villages:
                    impot += i.percevoir_impots()
                self.gamecontroller.joueur.augmenter_ressources(impot)
                self.gamecontroller.joueur.village_noble.produire_ressources()
                self.ajouter_evenement("Action exécutée: Impot")
                self.gamecontroller.appliquer_evenements(self.gamecontroller.joueur.village_noble.habitants)
                self.mettre_a_jour_infos()
            
            elif self.action_selectionnee == "paysan" or self.action_selectionnee == "roturier":
                immigration = Immigration(self.gamecontroller.joueur)
                if self.action_selectionnee == "roturier":
                    immigration.immigrer("roturier")
                elif self.action_selectionnee == "paysan":
                    immigration.immigrer("paysan")
                self.ajouter_evenement("Action exécutée: Immigration")

            self.action_selectionnee = None
            self.reset_bouton_couleurs()
            """reinitialiser les selections des cases"""
            from .map import Map
            liste = []
            for i in self.map.highlighted_cells:
                liste.append(i)
            for j in liste:
                self.map.unhighlight_cell(j[0],j[1])
            self.map.selected_villages = []
            self.gamecontroller.tour += 1
            self.mettre_a_jour_infos()
            self.gamecontroller.joueur.village_noble.afficher_statut()
    