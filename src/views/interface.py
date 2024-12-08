import tkinter as tk
from tkinter import font, Toplevel, ttk
from ..models import *
from src.controllers import *

class JeuInterface:
    def __init__(self, root, main_frame, game_controller):
        self.root = root
        self.main_frame = main_frame
        self.gamecontroller = game_controller
        self.root.title("Jeu Médiéval")
        self.root.geometry("900x600")
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
        self.map = Map(self.map_frame, self.gamecontroller, rows=10, cols=10, case_size=50)"""

        # Cadre principal avec deux colonnes
        self.main_content = tk.Frame(self.main_frame, bg="#2E2E2E")
        self.main_content.pack(expand=True, fill="both", padx=10, pady=10)

        # Colonne de gauche : carte
        self.map_frame = tk.Frame(self.main_content, bg="#2E2E2E")
        self.map_frame.pack(side=tk.LEFT, expand=True, fill="both")
        from .map import Map
        self.map = Map(self.map_frame, self.gamecontroller, rows=10, cols=10, case_size=50)
        self.map.interface = self

        # Colonne de droite : cadre principal pour les informations et le journal
        self.right_frame = tk.Frame(self.main_content, width=200, bg="#3A3A3A")
        self.right_frame.pack(side=tk.RIGHT, fill="y", padx=5)

        # Cadre pour les informations du village
        self.village_info_frame = tk.Frame(self.right_frame, bg="#2E2E2E", height=110)
        self.village_info_frame.pack_propagate(False)
        self.village_info_frame.pack(fill="x", pady=5, padx=5)
        self.action_bouton_selectionnee = None

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
        game_controller.set_interface(self)
        #afficher toutes les informations des nobles
        for i in self.gamecontroller.nobles:
            i.__str__()

        

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
        self.armee_label = tk.Label(self.info_frame, text=f"Armée : {len(self.gamecontroller.joueur.armee)} soldats", bg="#3A3A3A", fg="#F7F7F7", font=label_font)
        self.armee_label.pack(side="left", padx=15)
    
    def mettre_a_jour_infos(self):
        """Met à jour l'interface avec les infos actuelles du jeu."""
        # Accède aux informations du joueur et du village depuis `etat_du_jeu`
        self.argent_label.config(text=f"Argent : {self.gamecontroller.joueur.argent}")
        self.ressources_label.config(text=f"Ressources : {self.gamecontroller.joueur.ressources}")
        self.population_label.config(text=f"Nombre d'habitants : {self.gamecontroller.obtenir_nombre_total_personnes(self.gamecontroller.joueur)}")
        self.tour_label.config(text=f"Tour : {self.gamecontroller.tour}")
        self.armee_label.config(text=f"Armée : {len(self.gamecontroller.joueur.armee)} soldats")

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
        for widget in self.village_info_frame.winfo_children():
            widget.destroy()
        self.village_info_label = tk.Label(
            self.village_info_frame,
            text="CTRL + Clique droit sur un village pour voir ses informations",
            bg="#2E2E2E",
            fg="#F7F7F7",
            font=("Helvetica", 12),
            wraplength=200,
            justify="left",
        )
        self.village_info_label.pack(fill="both", expand=True, padx=3, pady=(0,0))
        if village:
            infos = (
                f"              {village.nom}\n\n"
                f"Population : {village.population}\n"
                f"Ressources habitants : {village.total_ressources}\n"
                f"Argent habitants : {village.total_argent}"
                #f"Seigneur : {village.seigneur.nom if village.seigneur else 'Aucun'}"
            )
        else:
            infos = "Clique droit sur un village pour voir ses informations"

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

        # Bouton Immigration
        self.immigration_bouton = tk.Button(
            self.actions_frame,
            text="Immigration",
            command=self.afficher_options_immigration,
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
        self.immigration_bouton.pack(side="left", padx=10, pady=5)
        
        # Bouton recruter
        self.recruter_bouton = tk.Button(
            self.actions_frame,
            text="recruter",
            command=self.afficher_options_recruter,
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
        self.recruter_bouton.pack(side="left", padx=10, pady=5)

        # Bouton pour acheter case
        self.acheter_case_bouton = tk.Button(
            self.actions_frame,
            text="acheter",
            command=lambda: self.selectionner_action("acheter_case"),
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
        self.acheter_case_bouton.pack(side="left", padx=10, pady=5)
        
        # Bouton pour declarer la guerre
        self.guerre_bouton = tk.Button(
            self.actions_frame,
            text="guerre",
            command=lambda: self.selectionner_action("guerre"),
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
        self.guerre_bouton.pack(side="left", padx=10, pady=5)
        
        

    def afficher_options_immigration(self):
        """
        Affiche deux boutons (Paysan et Roturier) dans `village_info_frame`
        pour sélectionner une option d'immigration.
        """
        if self.action_selectionnee == "paysan" or self.action_selectionnee == "roturier":
            self.action_selectionnee = None
            self.reset_bouton_couleurs()
            return
        # Vider le contenu précédent de `village_info_frame`
        for widget in self.village_info_frame.winfo_children():
            widget.destroy()

        if self.action_bouton_selectionnee == "immigration":
            self.mettre_a_jour_infos_village(self.map.village_affiché)
            self.action_bouton_selectionnee = None
        else:
            # Bouton "Paysan"
            paysan_bouton = tk.Button(
                self.village_info_frame,
                text="Paysan (-1 argent)",
                command=lambda: self.selectionner_action("paysan"),
                font=("Helvetica", 12),
                bg="#1C6E8C",
                fg="white",
                activebackground="#145374",
                activeforeground="white",
                bd=0
            )
            paysan_bouton.pack(side="top", pady=15, padx=10)

            # Bouton "Roturier"
            roturier_bouton = tk.Button(
                self.village_info_frame,
                text="Roturier (-2 argent)",
                command=lambda: self.selectionner_action("roturier"),
                font=("Helvetica", 12),
                bg="#1C6E8C",
                fg="white",
                activebackground="#145374",
                activeforeground="white",
                bd=0
            )
            roturier_bouton.pack(side="top", pady=5, padx=10)
            self.action_bouton_selectionnee = "immigration"

    def afficher_options_recruter(self):
        """
        Affiche deux boutons (Paysan et Roturier) dans `village_info_frame`
        pour sélectionner une option d'immigration.
        """
        if self.action_selectionnee == "infanterie" or self.action_selectionnee == "cavalier":
            self.action_selectionnee = None
            self.reset_bouton_couleurs()
            return
        
        # Vider le contenu précédent de `village_info_frame`
        for widget in self.village_info_frame.winfo_children():
            widget.destroy()

        if self.action_bouton_selectionnee == "recruter":
                self.mettre_a_jour_infos_village(self.map.village_affiché)
                self.action_bouton_selectionnee = None
        
        else:
            # Bouton "infanterie"
            infanterie_bouton = tk.Button(
                self.village_info_frame,
                text="infanterie (-5 argent)",
                command=lambda: self.selectionner_action("infanterie"),
                font=("Helvetica", 12),
                bg="#1C6E8C",
                fg="white",
                activebackground="#145374",
                activeforeground="white",
                bd=0
            )
            infanterie_bouton.pack(side="top", pady=15, padx=10)

            # Bouton "cavalier"
            cavalier_bouton = tk.Button(
                self.village_info_frame,
                text="cavalier (-10 argent)",
                command=lambda: self.selectionner_action("cavalier"),
                font=("Helvetica", 12),
                bg="#1C6E8C",
                fg="white",
                activebackground="#145374",
                activeforeground="white",
                bd=0
            )
            cavalier_bouton.pack(side="top", pady=5, padx=10)
            self.action_bouton_selectionnee = "recruter"
    
    def selectionner_action(self, action):
        if self.action_selectionnee == action:
            self.action_selectionnee = None
            self.map.selected_action = None  # Réinitialiser l'action sur la carte
            self.map.selected_villages = []
            self.map.territoire_selectionne = []
            self.reset_bouton_couleurs()
            
        else:
            self.action_selectionnee = action
            self.map.selected_action = action  # Définir l'action sélectionnée
            self.map.selected_villages = []
            self.map.territoire_selectionne = []
            self.action_bouton_selectionnee = action
            self.reset_bouton_couleurs()
            if action == "impot":
                self.impot_bouton.config(bg="#3498DB")
                self.action_bouton_selectionnee = None
            #elif action == "recruter":
                #self.recruter_bouton.config(bg="#3498DB")
            #elif action == "immigration":
                #self.immigration_bouton.config(bg="#3498DB")
            elif action == "paysan" or action == "roturier":
                self.immigration_bouton.config(bg="#3498DB")
            elif action == "infanterie" or action == "cavalier":
                self.recruter_bouton.config(bg="#3498DB")
            elif action == "acheter_case":
                self.acheter_case_bouton.config(bg="#3498DB")
            elif action == "guerre":
                self.guerre_bouton.config(bg="#3498DB")
            self.mettre_a_jour_infos_village(self.map.village_affiché)
            
        liste = []
        for i in self.map.highlighted_cases:
            liste.append(i)
        for j in liste:
            self.map.unhighlight_case(j[0],j[1])
        self.map.selected_villages = []

    def reset_bouton_couleurs(self):
        self.impot_bouton.config(bg="#1C6E8C")
        self.immigration_bouton.config(bg="#1C6E8C")
        self.recruter_bouton.config(bg="#1C6E8C")
        self.acheter_case_bouton.config(bg="#1C6E8C")
        self.guerre_bouton.config(bg="#1C6E8C")

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

    def afficher_tour_journal(self):
        """Affiche le tour actuel dans le journal du jeu."""
        self.ajouter_evenement("- - - - - - - - - - - - - - -")
        self.ajouter_evenement(f"|           Tour {self.gamecontroller.tour}          |")
        self.ajouter_evenement("- - - - - - - - - - - - - - -")

    def executer_action_selectionnee(self):
        from src.models import Immigration, Seigneur
        if self.action_selectionnee != None:
            if self.action_selectionnee == "impot":
                if self.map.selected_villages != []:
                    self.afficher_tour_journal()
                    self.ajouter_evenement("Action exécutée: Impot")
                    impot = 0
                    impot = self.gamecontroller.joueur.percevoir_impot(self.map.selected_villages)
                    self.ajouter_evenement(f"Impôt perçu: {impot}\n")
                    #self.gamecontroller.appliquer_evenements(self.gamecontroller.joueur.village_noble.habitants)
                    self.mettre_a_jour_infos()
                    self.finir_tour()
                else:
                    self.ajouter_evenement("Vous devez choisir un village")
            elif self.action_selectionnee == "acheter_case":
                if self.map.territoire_selectionne != []:
                    self.afficher_tour_journal()
                    for i in self.map.territoire_selectionne:
                        i.acheter(self.gamecontroller.joueur)
                    self.ajouter_evenement("Action exécutée: Achat de case")
                    self.finir_tour()
                else:
                    self.ajouter_evenement("Vous devez choisir un territoire")
            
            elif self.action_selectionnee == "paysan" or self.action_selectionnee == "roturier":
                if self.map.selected_villages != []:
                    self.afficher_tour_journal()
                    for village in self.map.selected_villages:
                        immigration = Immigration(village.noble)
                        if self.action_selectionnee == "roturier":
                            immigration.immigrer("roturier")
                        elif self.action_selectionnee == "paysan":
                            immigration.immigrer("paysan")
                    self.ajouter_evenement("Action exécutée: Immigration")
                    self.finir_tour()
                else:
                    self.ajouter_evenement("Vous devez choisir un village")

            elif self.action_selectionnee == "infanterie" or self.action_selectionnee == "cavalier":
                from src.models import Soldat
                self.afficher_tour_journal()
                if self.action_selectionnee == "infanterie":
                    self.gamecontroller.joueur.recruter(Soldat("infanterie", 5, "infanterie"))
                elif self.action_selectionnee == "cavalier":
                    self.gamecontroller.joueur.recruter(Soldat("cavalier", 10, "cavalier"))
                self.ajouter_evenement("Action exécutée: Recrutement")
                self.finir_tour()
            
            elif self.action_selectionnee == "guerre":
                if self.map.selected_villages != []:
                    if self.map.territoires_adjacents(self.gamecontroller.joueur, self.map.selected_villages[0].proprietaire):
                        self.afficher_tour_journal()
                        self.gamecontroller.guerre(self.gamecontroller.joueur, self.map.selected_villages[0].proprietaire)
                        print("seigneur : ",isinstance(self.gamecontroller.joueur,Seigneur))

                        self.ajouter_evenement("Action exécutée: Guerre")
                        self.finir_tour()
                    else:
                        self.ajouter_evenement("Vous ne pouvez pas déclarer la guerre à ce village")
                else:
                    self.ajouter_evenement("Vous devez choisir un village")
    
    def finir_tour(self):
        """reset les actions selectionnées"""
        self.action_selectionnee = None
        self.action_bouton_selectionnee = None
        self.reset_bouton_couleurs()
        """reinitialiser les selections des cases"""
        from .map import Map
        liste = []
        for i in self.map.highlighted_cases:
            liste.append(i)
        for j in liste:
            self.map.unhighlight_case(j[0],j[1])
        self.map.selected_action = None
        self.map.selected_villages = []
        self.map.territoire_selectionne = []

        self.gamecontroller.tour_suivant()
        
        self.mettre_a_jour_infos()
        #self.gamecontroller.joueur.village_noble.afficher_statut()
        self.mettre_a_jour_infos_village(self.map.village_affiché)
        self.map.mettre_a_jour_bordures()
        
    