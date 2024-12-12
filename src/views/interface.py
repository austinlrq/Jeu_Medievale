import tkinter as tk
from tkinter import font, Toplevel, ttk
from ..models import *
from ..views.settingsinterface import SettingsInterface
from src.controllers import *
import customtkinter

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

        # Gestion de l'événement Échap pour ouvrir le menu pause
        self.root.bind("<Escape>", self.ouvrir_menu_pause)

        ### MENU PAUSE ###
        # Cadre du menu de pause (invisible au départ)
        # Créer un fond 
        # self.menu_pause_canvas.create_rectangle(0, 0, self.root.winfo_width(), self.root.winfo_height()) 
        # self.menu_pause_canvas.create_image(0,0,image=tk.PhotoImage(file="images/pause.png")) 
        # Cadre pour les boutons dans le menu de pause
        self.menu_frame = tk.Frame(self.root)

        # Bouton Continuer
        continue_button = tk.Button(self.menu_frame, text="Continuer", command=self.continuer_jeu, width=20, height=2)
        continue_button.pack(pady=10)

        # Bouton Paramètres
        settings_button = tk.Button(self.menu_frame, text="Paramètres", command=self.ouvrir_parametres, width=20, height=2)
        settings_button.pack(pady=10)

        # Bouton Quitter
        quit_button = tk.Button(self.menu_frame, text="Quitter", command=self.quitter_jeu, width=20, height=2)
        quit_button.pack(pady=10)
        ####

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
        self.village_info_frame = tk.Frame(self.right_frame, bg="#2E2E2E", height=160)
        self.village_info_frame.pack_propagate(False)
        self.village_info_frame.pack(fill="x", pady=5, padx=5)
        self.action_bouton_selectionnee = None

        self.village_info_label = tk.Label(
            self.village_info_frame,
            text="Ctrl + Clique droit sur un village pour voir ses informations",
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

    
    def ouvrir_menu_pause(self, event=None):
        """Affiche le menu de pause (superposé à l'interface du jeu)"""
        self.menu_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1.0, relheight=1.0)  # Afficher le menu de pause

    def continuer_jeu(self):
        """Cache le menu de pause et reprend le jeu"""
        self.menu_frame.place_forget()  # Cache le menu de pause
        self.map.drag_manager.load_sensi()

    def ouvrir_parametres(self):
        """Ouvre une fenêtre pour les paramètres du jeu"""
        self.settings = SettingsInterface(self.root, self.main_frame)
        self.settings.creer_visu(True)  # Crée l'interface des paramètres

    def quitter_jeu(self):
        """Quitte le jeu"""
        self.root.quit()

    def afficher_informations(self):
        label_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.argent_label = tk.Label(self.info_frame, text=f"Argent : {self.gamecontroller.joueur.argent}", bg="#3A3A3A", fg="#F7F7F7", font=label_font)
        self.argent_label.pack(side="left", padx=15)
        self.ressources_label = tk.Label(self.info_frame, text=f"Ressources : {self.gamecontroller.joueur.ressources}", bg="#3A3A3A", fg="#F7F7F7", font=label_font)
        self.ressources_label.pack(side="left", padx=15)
        self.population_label = tk.Label(self.info_frame, text=f"Habitants : {self.gamecontroller.joueur.village_noble.population}/{self.gamecontroller.joueur.capacite_habitants}", bg="#3A3A3A", fg="#F7F7F7", font=label_font)
        self.population_label.pack(side="left", padx=15)
        self.tour_label = tk.Label(self.info_frame, text=f"Tour : {self.gamecontroller.tour}", bg="#3A3A3A", fg="#F7F7F7", font=label_font)
        self.tour_label.pack(side="right", padx=15)
        self.armee_label = tk.Label(self.info_frame, text=f"Soldats : {len(self.gamecontroller.joueur.armee)}/{self.gamecontroller.joueur.capacite_soldats}", bg="#3A3A3A", fg="#F7F7F7", font=label_font)
        self.armee_label.pack(side="left", padx=15)
    
    def mettre_a_jour_infos(self):
        """Met à jour l'interface avec les infos actuelles du jeu."""
        # Accède aux informations du joueur et du village depuis `etat_du_jeu`
        self.argent_label.config(text=f"Argent : {self.gamecontroller.joueur.argent}")
        self.ressources_label.config(text=f"Ressources : {self.gamecontroller.joueur.ressources}")
        self.population_label.config(text=f"Habitants : {self.gamecontroller.obtenir_nombre_total_personnes(self.gamecontroller.joueur)}/{self.gamecontroller.joueur.capacite_habitants}")
        self.tour_label.config(text=f"Tour : {self.gamecontroller.tour}")
        self.armee_label.config(text=f"Soldats : {len(self.gamecontroller.joueur.armee)}/{self.gamecontroller.joueur.capacite_soldats}")

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
            text="Ctrl + Clique droit sur un village pour voir ses informations",
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
            infos = "Ctrl + Clique droit sur un village pour voir ses informations"

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

        # Bouton marché
        self.marche_bouton = tk.Button(
            self.actions_frame,
            text="Marché",
            command=lambda: self.afficher_options_marche(),
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
        self.marche_bouton.pack(side="left", padx=10, pady=5)
        
        # Bouton recruter
        self.recruter_bouton = tk.Button(
            self.actions_frame,
            text="Recruter",
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

        
        # Bouton pour contruire
        self.construire_bouton = tk.Button(
            self.actions_frame,
            text="Construire",
            command=lambda: self.afficher_options_construire("contruire"),
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
        self.construire_bouton.pack(side="left", padx=10, pady=5)
        
        # Bouton pour declarer la guerre
        self.guerre_bouton = tk.Button(
            self.actions_frame,
            text="Guerre",
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
        

    def afficher_options_recruter(self):
        """
        Affiche deux colonnes de boutons dans `village_info_frame`
        pour sélectionner une option de recrutement.
        """
        if self.action_selectionnee in ["infanterie", "cavalier", "paysan", "roturier"]:
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
            # Cadre pour les deux colonnes
            columns_frame = tk.Frame(self.village_info_frame, bg="#2E2E2E")
            columns_frame.pack(fill="both", expand=True)

            # Colonne de gauche
            left_column = tk.Frame(columns_frame, bg="#2E2E2E", width=100)
            left_column.pack(side="left", fill="both", expand=True, padx=2)

            separateur = ttk.Separator(columns_frame, orient="vertical")
            separateur.pack(side="left", fill="y", pady=2)

            # Colonne de droite
            right_column = tk.Frame(columns_frame, bg="#2E2E2E", width=100)
            right_column.pack(side="right", fill="both", expand=True, padx=2)

            texte = tk.Label(left_column, text="Village", bg="#2E2E2E", fg="#F7F7F7", font=("Helvetica", 12))
            texte.pack(pady=10)

            texte2 = tk.Label(right_column, text="Armée", bg="#2E2E2E", fg="#F7F7F7", font=("Helvetica", 12))
            texte2.pack(pady=10)

            # Bouton "Paysan"
            paysan_bouton = tk.Button(
                left_column,
                text="Paysan (-1)",
                command=lambda: self.selectionner_action("paysan"),
                font=("Helvetica", 12),
                bg="#1C6E8C",
                fg="white",
                activebackground="#145374",
                activeforeground="white",
                bd=0
            )
            paysan_bouton.pack(side="top", pady=5, padx=10)

            # Bouton "Roturier"
            roturier_bouton = tk.Button(
                left_column,
                text="Roturier (-2)",
                command=lambda: self.selectionner_action("roturier"),
                font=("Helvetica", 12),
                bg="#1C6E8C",
                fg="white",
                activebackground="#145374",
                activeforeground="white",
                bd=0
            )
            roturier_bouton.pack(side="top", pady=5, padx=10)

            # Bouton "Infanterie"
            infanterie_bouton = tk.Button(
                right_column,
                text="Infanterie (-5)",
                command=lambda: self.selectionner_action("infanterie"),
                font=("Helvetica", 12),
                bg="#1C6E8C",
                fg="white",
                activebackground="#145374",
                activeforeground="white",
                bd=0
            )
            infanterie_bouton.pack(side="top", pady=5, padx=10)

            # Bouton "Cavalier"
            cavalier_bouton = tk.Button(
                right_column,
                text="Cavalier (-10)",
                command=lambda: self.selectionner_action("cavalier"),
                font=("Helvetica", 12),
                bg="#1C6E8C",
                fg="white",
                activebackground="#145374",
                activeforeground="white",
                bd=0
            )
            cavalier_bouton.pack(side="top", pady=5, padx=10)

            texte_cout = tk.Label(self.village_info_frame, text="Cout: argent", bg="#2E2E2E", fg="#F7F7F7", font=("Helvetica", 8))
            texte_cout.pack(pady=10)

            self.action_bouton_selectionnee = "recruter"
            
            
    def afficher_options_construire(self,action):
        if self.action_selectionnee == "terrain" or self.action_selectionnee == "habitation" or self.action_selectionnee == "camp":
            self.action_selectionnee = None
            self.reset_bouton_couleurs()
            return
        
        # Vider le contenu précédent de `village_info_frame`
        for widget in self.village_info_frame.winfo_children():
            widget.destroy()

        if self.action_bouton_selectionnee == "construire":
                self.mettre_a_jour_infos_village(self.map.village_affiché)
                self.action_bouton_selectionnee = None
        
        else:
            # Cadre pour les deux colonnes
            columns_frame = tk.Frame(self.village_info_frame, bg="#2E2E2E")
            columns_frame.pack(fill="both", expand=True)

            # Colonne de gauche
            left_column = tk.Frame(columns_frame, bg="#2E2E2E", width=100)
            left_column.pack(side="left", fill="both", expand=True, padx=2)

            separateur = tk.ttk.Separator(columns_frame, orient="vertical")
            separateur.pack(side="left", fill="y", pady=2)

            # Colonne de droite
            right_column = tk.Frame(columns_frame, bg="#2E2E2E", width=100)
            right_column.pack(side="right", fill="both", expand=True, padx=2)

            texte = tk.Label(left_column, text="Territoire", bg="#2E2E2E", fg="#F7F7F7", font=("Helvetica", 12))
            texte.pack(pady=10)

            texte2 = tk.Label(right_column, text="Batiments", bg="#2E2E2E", fg="#F7F7F7", font=("Helvetica", 12))
            texte2.pack(pady=10)


            # Bouton "infanterie"
            terrain_bouton = tk.Button(
                left_column,
                text="Terrain (-5)",
                command=lambda: self.selectionner_action("terrain"),
                font=("Helvetica", 12),
                bg="#1C6E8C",
                fg="white",
                activebackground="#145374",
                activeforeground="white",
                bd=0
            )
            terrain_bouton.pack(side="top", pady=5, padx=10)

            # Bouton "cavalier"
            habitation_bouton = tk.Button(
                right_column,
                text="Habitat (-10)",
                command=lambda: self.selectionner_action("habitation"),
                font=("Helvetica", 12),
                bg="#1C6E8C",
                fg="white",
                activebackground="#145374",
                activeforeground="white",
                bd=0
            )
            habitation_bouton.pack(side="top", pady=5, padx=10)
            
            camp_bouton = tk.Button(
                right_column,
                text="Camp (-10)",
                command=lambda: self.selectionner_action("camp"),
                font=("Helvetica", 12),
                bg="#1C6E8C",
                fg="white",
                activebackground="#145374",
                activeforeground="white",
                bd=0
            )
            camp_bouton.pack(side="top", pady=5, padx=10)
            
            texte_cout = tk.Label(self.village_info_frame, text="Cout: argent", bg="#2E2E2E", fg="#F7F7F7", font=("Helvetica", 8))
            texte_cout.pack(pady=10)

            self.action_bouton_selectionnee = "construire"
    
    def afficher_options_marche(self):
        for widget in self.village_info_frame.winfo_children():
            widget.destroy()
        """texte = tk.Label(self.village_info_frame, text="Marché", bg="#2E2E2E", fg="#F7F7F7", font=("Helvetica", 12))
        texte.pack(pady=10)
        slider = customtkinter.CTkSlider(master=self.village_info_frame, from_=0, to=self.gamecontroller.joueur.argent, orientation="horizontal")
        slider.pack(pady=10)
        bouton = tk.Button(self.village_info_frame, text="Acheter", command=lambda: self.acheter_ressources(slider.get()), font=("Helvetica", 12, "bold"), bg="#1C6E8C", fg="white", activebackground="#145374", activeforeground="white", bd=0)
        bouton.pack(pady=10)"""
        
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
            elif action == "infanterie" or action == "cavalier" or action == "paysan" or action == "roturier":
                self.recruter_bouton.config(bg="#3498DB")
            elif action == "guerre":
                self.guerre_bouton.config(bg="#3498DB")
            elif action == "terrain" or action == "habitation" or action == "camp":
                self.construire_bouton.config(bg="#3498DB")
            self.mettre_a_jour_infos_village(self.map.village_affiché)
            
        liste = []
        for i in self.map.highlighted_cases:
            liste.append(i)
        for j in liste:
            self.map.unhighlight_case(j[0],j[1])
        self.map.selected_villages = []

    def reset_bouton_couleurs(self):
        self.impot_bouton.config(bg="#1C6E8C")
        self.recruter_bouton.config(bg="#1C6E8C")
        self.guerre_bouton.config(bg="#1C6E8C")
        self.construire_bouton.config(bg="#1C6E8C")

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
        if self.gamecontroller.tour <= 9:
            self.ajouter_evenement("- - - - - - - - - - - - - - -")
            self.ajouter_evenement(f"|           Tour {self.gamecontroller.tour}          |")
            self.ajouter_evenement("- - - - - - - - - - - - - - -")
        elif self.gamecontroller.tour <= 99:
            self.ajouter_evenement("- - - - - - - - - - - - - - -")
            self.ajouter_evenement(f"|          Tour {self.gamecontroller.tour}          |")
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
            
            
            elif self.action_selectionnee == "paysan" or self.action_selectionnee == "roturier":
                if self.map.selected_villages != []:
                    self.ajouter_evenement("Action exécutée: Immigration\n")
                    for village in self.map.selected_villages:
                        immigration = Immigration(village.noble)
                        if self.gamecontroller.obtenir_nombre_total_personnes(self.gamecontroller.joueur) >= self.gamecontroller.joueur.capacite_habitants:
                            self.ajouter_evenement("Vous avez atteint votre capacité maximale d'habitants")
                            return
                        if self.action_selectionnee == "roturier":
                            if self.gamecontroller.joueur.argent < 2:
                                self.ajouter_evenement("Vous n'avez pas assez d'argent pour immigrer un roturier")
                                return
                            self.afficher_tour_journal()
                            immigration.immigrer("roturier")
                            self.ajouter_evenement("Roturier immigré\n")
                        elif self.action_selectionnee == "paysan":
                            if self.gamecontroller.joueur.argent < 1:
                                self.ajouter_evenement("Vous n'avez pas assez d'argent pour immigrer un paysan")
                                return
                            self.afficher_tour_journal()
                            immigration.immigrer("paysan")
                            self.ajouter_evenement("Paysan immigré\n")
                    
                    self.finir_tour()
                else:
                    self.ajouter_evenement("Vous devez choisir un village")

            elif self.action_selectionnee == "infanterie" or self.action_selectionnee == "cavalier":
                from src.models import Soldat
                if self.gamecontroller.joueur.capacite_soldats <= len(self.gamecontroller.joueur.armee):
                    self.ajouter_evenement("Vous avez atteint votre capacité maximale de soldats")
                    return
                if self.gamecontroller.joueur.argent < 5 and self.action_selectionnee == "infanterie":
                    self.ajouter_evenement("Vous n'avez pas assez d'argent pour recruter un soldat")
                    return
                elif self.gamecontroller.joueur.argent < 10 and self.action_selectionnee == "cavalier":
                    self.ajouter_evenement("Vous n'avez pas assez d'argent pour recruter un soldat")
                    return
                self.afficher_tour_journal()
                self.ajouter_evenement("Action exécutée: Recrutement\n")
                if self.action_selectionnee == "infanterie":
                    self.gamecontroller.joueur.recruter(Soldat("infanterie", 5, "infanterie"))
                    self.ajouter_evenement("Soldat recruté: infanterie\n")
                elif self.action_selectionnee == "cavalier":
                    self.gamecontroller.joueur.recruter(Soldat("cavalier", 10, "cavalier"))
                    self.ajouter_evenement("Soldat recruté: cavalier\n")
                
                self.finir_tour()
            
            elif self.action_selectionnee == "guerre":
                if self.map.selected_villages != []:
                    if self.map.territoires_adjacents(self.gamecontroller.joueur, self.map.selected_villages[0].proprietaire):
                        self.afficher_tour_journal()
                        self.ajouter_evenement("Action exécutée: Guerre\n")
                        self.gamecontroller.guerre(self.gamecontroller.joueur, self.map.selected_villages[0].proprietaire)
                        print("seigneur : ",isinstance(self.gamecontroller.joueur,Seigneur))
                        self.finir_tour()
                    else:
                        self.ajouter_evenement("Vous ne pouvez pas déclarer la guerre à ce village")
                else:
                    self.ajouter_evenement("Vous devez choisir un village")
                    
                    
            elif self.action_selectionnee == "terrain" or self.action_selectionnee == "habitation" or self.action_selectionnee == "camp":
                if self.map.territoire_selectionne != []:
                    if self.action_selectionnee == "terrain":
                        if self.gamecontroller.joueur.argent < len(self.map.territoire_selectionne)*5:
                            self.ajouter_evenement("Vous n'avez pas assez d'argent pour acheter ces terrains")
                            return
                        self.afficher_tour_journal()
                        self.ajouter_evenement("Action exécutée: Construction\n")
                        for i in self.map.territoire_selectionne:
                            i.acheter(self.gamecontroller.joueur)
                    elif self.action_selectionnee == "habitation":
                        if self.gamecontroller.joueur.argent < 10:
                            self.ajouter_evenement("Vous n'avez pas assez d'argent pour construire cette habitation")
                            return
                        self.afficher_tour_journal()
                        self.ajouter_evenement("Action exécutée: Construction\n")
                        self.gamecontroller.construire(self.gamecontroller.joueur,self.map.territoire_selectionne[0],"habitation")
                    elif self.action_selectionnee == "camp":
                        if self.gamecontroller.joueur.argent < 10:
                            self.ajouter_evenement("Vous n'avez pas assez d'argent pour construire ce camp")
                            return
                        self.afficher_tour_journal()
                        self.ajouter_evenement("Action exécutée: Construction\n")
                        self.gamecontroller.construire(self.gamecontroller.joueur,self.map.territoire_selectionne[0],"camp")                    
                    self.finir_tour()
                else:
                    self.ajouter_evenement("Vous devez choisir un territoire")
                
    
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
        self.map.dessiner_map_visible()
    