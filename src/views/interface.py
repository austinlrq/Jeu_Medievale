import tkinter as tk
from tkinter import font, Toplevel, ttk, filedialog, messagebox
import json
from ..models import *
from ..views.settingsinterface import SettingsInterface
from src.controllers import *
import customtkinter

class JeuInterface:
    def __init__(self, root, main_frame, game_controller, map_data= None):
        self.root = root
        self.main_frame = main_frame
        self.gamecontroller = game_controller
        self.root.title("La Guerre des Frontières")
        self.root.geometry("900x600")
        self.root.configure(bg="#2E2E2E")
        self.root.resizable(True, True)
        self.action_selectionnee = None
        self.quantite_achete_vend = 0

        # Cadre pour l'affichage des informations en haut
        self.info_frame = tk.Frame(self.main_frame, height=50, bg="#3A3A3A")
        self.info_frame.pack(fill="x", pady=0)
        self.afficher_bouton_pause()
        self.afficher_informations()

        # Gestion de l'événement Échap pour ouvrir le menu pause
        self.root.bind("<Escape>", self.ouvrir_menu_pause)
        self.sauvegarde = False

        # Cadre principal avec deux colonnes
        self.main_content = tk.Frame(self.main_frame, bg="#2E2E2E")
        self.main_content.pack(expand=True, fill="both", padx=10, pady=10)

        # Colonne de gauche : carte
        self.map_frame = tk.Frame(self.main_content, bg="#2E2E2E")
        self.map_frame.pack(side=tk.LEFT, expand=True, fill="both")
        from .map import Map
        self.map = Map(self.map_frame, self.gamecontroller, self, case_size=50, map_data = map_data)
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
            text="Ctrl + Clique gauche sur un village pour voir ses informations",
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
        self.ajouter_evenement("- - - - - - - - - - - - - - -")
        self.ajouter_evenement(f"|     Debut de la partie    |")
        self.ajouter_evenement("- - - - - - - - - - - - - - -\n")

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

    def sauvegarder_partie(self):
        """Sauvegarde l'état actuel de la partie dans un fichier JSON."""
        try:
            # Récupérer les données nécessaires
            etat_partie = {
                "villages": [village.to_dict() for village in self.gamecontroller.villages],  # Vous devez définir une méthode to_dict() pour Village
                "joueur": self.gamecontroller.joueur.to_dict(),  # Méthode to_dict() pour le joueur
                "map": self.map.to_dict(),       # Méthode to_dict() pour la carte
                "tour": self.gamecontroller.tour
            }
            
            # Ouvrir une boîte de dialogue pour choisir l'emplacement de sauvegarde
            fichier_sauvegarde = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json")],
                title="Enregistrer la partie"
            )
            
            if fichier_sauvegarde:
                # Sauvegarder les données dans un fichier JSON
                with open(fichier_sauvegarde, 'w', encoding='utf-8') as fichier:
                    json.dump(etat_partie, fichier, indent=4, ensure_ascii=False)
                self.ajouter_evenement("Partie sauvegardée avec succès !")
                self.sauvegarde = True
            else:
                self.ajouter_evenement("Sauvegarde annulée.")
                self.sauvegarde = False
        except Exception as e:
            self.ajouter_evenement(f"Erreur lors de la sauvegarde : {e}")
            
    def retourner_menu(self):
        from src.views import MenuPrincipal 
        if self.voulez_sauvegarder():
            self.sauvegarder_partie()
            self.main_frame.pack_forget()
            MenuPrincipal(self.root)
        else:
            self.main_frame.pack_forget()
            MenuPrincipal(self.root)
        
    def ouvrir_menu_pause(self, event=None):
        """Affiche le menu de pause (superposé à l'interface du jeu)"""
        self.root.bind("<Escape>", self.continuer_jeu)
        
        try:
            # Supprimer Aideinterface si elle existe
            self.AideInterface.quitter()
        except:
            pass
        
        self.menu_frame = tk.Frame(self.root,bg="#2E2E2E")
        
        # Ajouter le bouton "Retour"
        self.bouton_quitter = tk.Button(
            self.menu_frame, 
            text="<  Retour", 
            command=self.continuer_jeu, 
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
        
        texte_menu = tk.Label(self.menu_frame, text="Menu Pause", font=("Helvetica", 24, "bold"), bg="#2E2E2E", fg="#F7F7F7", width=20, height=2)
        texte_menu.place(relx=0.5, rely=0.12, anchor="center")
        # Bouton Continuer
        continue_button = tk.Button(self.menu_frame, text="informations", command=self.show_help, width=20, height=2,
                                    font=("Helvetica", 16, "bold"),
                                    bg="#1C6E8C",
                                    fg="white",
                                    activebackground="#145374",
                                    activeforeground="white",
                                    bd=0)
        continue_button.place(relx=0.30, rely=0.35, anchor="center")

        # Bouton Paramètres
        settings_button = tk.Button(self.menu_frame, text="Paramètres", command=self.ouvrir_parametres, width=20, height=2,
                                    font=("Helvetica", 16, "bold"),
                                    bg="#1C6E8C",
                                    fg="white",
                                    activebackground="#145374",
                                    activeforeground="white",
                                    bd=0)
        settings_button.place(relx=0.30, rely=0.55, anchor="center")
        
        # Separateur
        separateur = ttk.Separator(self.menu_frame, orient="vertical")
        separateur.place(relx=0.5, rely=0.45, anchor="center", relheight=0.4)

        # Bouton Sauvegarder
        save_button = tk.Button(self.menu_frame, text="Sauvegarder", command=self.sauvegarder_partie, width=20, height=2,
                                    font=("Helvetica", 16, "bold"),
                                    bg="#1C6E8C",
                                    fg="white",
                                    activebackground="#145374",
                                    activeforeground="white",
                                    bd=0)
        save_button.place(relx=0.70, rely=0.35, anchor="center")
        
        # Bouton Retour au Menu
        retour_menu = tk.Button(self.menu_frame, text="Retour au Menu", command=self.retourner_menu, width=20, height=2,
                                    font=("Helvetica", 16, "bold"),
                                    bg="#1C6E8C",
                                    fg="white",
                                    activebackground="#145374",
                                    activeforeground="white",
                                    bd=0)
        retour_menu.place(relx=0.70, rely=0.55, anchor="center")

        # Bouton Quitter
        quit_button = tk.Button(self.menu_frame, text="Quitter", command=self.quitter_jeu, width=20, height=2,
                                    font=("Helvetica", 16, "bold"),
                                    bg="#D9455F",
                                    fg="white",
                                    activebackground="#145374",
                                    activeforeground="white",
                                    bd=0)
        quit_button.place(relx=0.5, rely=0.80, anchor="center")

        self.menu_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1.0, relheight=1.0)  # Afficher le menu de pause

    def continuer_jeu(self, event=None):
        """Cache le menu de pause et reprend le jeu"""
        try:
            # Supprimer Aideinterface si elle existe
            self.AideInterface.quitter()
        except:
            pass
        self.menu_frame.place_forget()  # Cache le menu de pause
        self.map.drag_manager.load_sensi()
        self.root.bind("<Escape>", self.ouvrir_menu_pause)

    def ouvrir_parametres(self):
        """Ouvre une fenêtre pour les paramètres du jeu"""
        self.settings = SettingsInterface(self.root, self.main_frame)
        self.settings.creer_visu(True)  # Crée l'interface des paramètres

    def quitter_jeu(self):
        """Quitte le jeu"""
        if self.voulez_sauvegarder():
            self.sauvegarder_partie()
        self.root.quit()
        
    def voulez_sauvegarder(self):
        if not self.sauvegarde: 
            return tk.messagebox.askyesno(title="Sauvegarde", message="Voulez vous sauvegarder avant de partir?")
        else:
            return False
    
    def show_help(self):
        # Afficher une boîte de message avec les explications du jeu
        from src.views import AideInterface
        #self.root.bind("<Escape>", self.continuer_jeu)
        self.AideInterface = AideInterface(self.root, self.main_frame)
        self.AideInterface.afficher()
        

    def afficher_bouton_pause(self):
        # Créer le canvas pour le point d'interrogation
        self.help_canvas = tk.Canvas(self.info_frame, width=30, height=30, bg="#3A3A3A", highlightthickness=0)
        self.help_canvas.pack(side="left", padx=0)  # Positionner en haut à gauche

        # Dessiner un carré avec des coins arrondis sans traits à l'intérieur
        radius = 5
        self.help_canvas.create_arc(5, 5, 5 + 2*radius, 5 + 2*radius, start=90, extent=90, fill="#3A3A3A", outline='white')
        self.help_canvas.create_arc(25 - 2*radius, 5, 25, 5 + 2*radius, start=0, extent=90, fill="#3A3A3A", outline='white')
        self.help_canvas.create_arc(25 - 2*radius, 25 - 2*radius, 25, 25, start=270, extent=90, fill="#3A3A3A", outline='white')
        self.help_canvas.create_arc(5, 25 - 2*radius, 5 + 2*radius, 25, start=180, extent=90, fill="#3A3A3A", outline='white')
        self.help_canvas.create_polygon(
            5 + radius, 5,
            25 - radius, 5,
            25, 5 + radius,
            25, 25 - radius,
            25 - radius, 25,
            5 + radius, 25,
            5, 25 - radius,
            5, 5 + radius,
            outline='white', fill="#3A3A3A"
        )

        # Dessiner les barres verticales pour le bouton pause
        self.help_canvas.create_rectangle(11, 10, 13, 20, fill="white", outline="white")
        self.help_canvas.create_rectangle(17, 10, 19, 20, fill="white", outline="white")

        # Rendre le canvas cliquable
        self.help_canvas.bind("<Button-1>", self.ouvrir_menu_pause)

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

    def mettre_a_jour_infos_village(self, case):
        """
        Met à jour les informations affichées sur le village sélectionné.
        """
        for widget in self.village_info_frame.winfo_children():
            widget.destroy()
        self.village_info_label = tk.Label(
            self.village_info_frame,
            text="Ctrl + Clique gauche sur un village pour voir ses informations",
            bg="#2E2E2E",
            fg="#F7F7F7",
            font=("Helvetica", 12),
            wraplength=200,
            justify="left",
            anchor="center"
        )
        self.village_info_label.pack(fill="both", expand=True, padx=3, pady=(0,0))
        
        if case:
            if not case.batiment:
                village = case.village
                infos = (
                    f"                {village.case.proprietaire.nom}\n\n"
                    f"Population : {village.population}\n"
                    f"Ressources habitants : {village.total_ressources}\n"
                    f"Argent habitants : {village.total_argent}"
                    #f"Seigneur : {village.seigneur.nom if village.seigneur else 'Aucun'}"
                )
            elif case.batiment == "camp":
                # Afficher que les informations de l'armée, soldats
                liste_inf=[]
                liste_cav=[]
                for i in case.proprietaire.armee:
                    if i.type_soldat == "Infanterie":
                        liste_inf+=[i]
                    elif i.type_soldat == "Cavalier":
                        liste_cav+=[i]
                if case.proprietaire != self.gamecontroller.joueur:
                    infos = (
                        f"      {case.proprietaire.nom}\n\n"
                        f"Soldats : {len(case.proprietaire.armee)}/{case.proprietaire.capacite_soldats}\n"
                        f"Infanterie : * * *\n"
                        f"Cavaliers : * * *\n"
                        f"Puissance : * * *"
                    )
                else:
                    infos = (
                        f"      {case.proprietaire.nom}\n\n"
                        f"Soldats : {len(case.proprietaire.armee)}/{case.proprietaire.capacite_soldats}\n"
                        f"Infanterie : {len(liste_inf)}\n"
                        f"Cavaliers : {len(liste_cav)}\n"
                        f"Puissance : {sum(soldat.force for soldat in case.proprietaire.armee)}"
                    )
        else:
            infos = "Ctrl + Clique gauche sur un village pour voir ses informations"

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
                text="Paysan (-5)",
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
                text="Roturier (-10)",
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
                text="Infanterie (-10)",
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
                text="Cavalier (-15)",
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

        if self.action_selectionnee in ["acheter", "vendre"]:
            self.action_selectionnee = None
            self.reset_bouton_couleurs()
            return
        
        for widget in self.village_info_frame.winfo_children():
            widget.destroy()

        if self.action_bouton_selectionnee == "marche":
            self.mettre_a_jour_infos_village(self.map.village_affiché)
            self.action_bouton_selectionnee = None
            return
        self.texte1 = None
        self.slider1 = None
        self.bouton1 = None
        self.texte2 = None
        self.slider2 = None
        self.bouton2 = None

        def clique_acheter():
            if getattr(self, 'texte1', None):
                return
            if getattr(self, 'texte2', None):
                self.texte2.destroy()
                self.texte2 = None
            if getattr(self, 'slider2', None):
                self.slider2.destroy()
                self.slider2 = None
            if getattr(self, 'bouton2', None):
                self.bouton2.destroy()
                self.bouton2 = None
            choix1.config(bg="#2E2E2E")
            choix2.config(bg="#3A3A3A")
            self.texte1 = tk.Label(self.village_info_frame, text="Achète : 0    -   Cout : 0", bg="#2E2E2E", fg="#F7F7F7", font=("Helvetica", 12))
            self.texte1.pack(side="top", pady=10)

            def update_label(value):
                self.texte1.config(text=f"Achète : {int(float(value)*1.2)}  -  Cout : {int(float(value))}")
                self.quantite_achete_vend = int(float(value))
            
            self.slider1 = customtkinter.CTkSlider(master=self.village_info_frame, from_=0, to=self.gamecontroller.joueur.argent, orientation="horizontal", command=update_label)
            self.slider1.pack(pady=10)
            
            self.bouton1 = tk.Button(self.village_info_frame, text="Acheter", command=lambda: self.selectionner_action("acheter"), font=("Helvetica", 12, "bold"), bg="#1C6E8C", fg="white", activebackground="#145374", activeforeground="white", bd=0)
            self.bouton1.pack(pady=10)

        def clique_vendre():
            if getattr(self, 'texte2', None):
                return
            choix1.config(bg="#3A3A3A")
            choix2.config(bg="#2E2E2E")
            if getattr(self, 'texte1', None):
                self.texte1.destroy()
                self.texte1 = None
            if getattr(self, 'slider1', None):
                self.slider1.destroy()
                self.slider1 = None
            if getattr(self, 'bouton1', None):
                self.bouton1.destroy()
                self.bouton1 = None
            self.texte2 = tk.Label(self.village_info_frame, text="Vend : 0  -   Pour : 0", bg="#2E2E2E", fg="#F7F7F7", font=("Helvetica", 12))
            self.texte2.pack(side="top", pady=10)
            
            def update_label(value):
                self.texte2.config(text=f"Vend : {int(float(value))}    -   Pour : {int(float(value)*0.8)}")
                self.quantite_achete_vend = int(float(value))
            
            self.slider2 = customtkinter.CTkSlider(master=self.village_info_frame, from_=0, to=self.gamecontroller.joueur.ressources, orientation="horizontal", command=update_label)
            self.slider2.pack(pady=10)
            
            self.bouton2 = tk.Button(self.village_info_frame, text="Vendre", command=lambda: self.selectionner_action("vendre"), font=("Helvetica", 12, "bold"), bg="#1C6E8C", fg="white", activebackground="#145374", activeforeground="white", bd=0)
            self.bouton2.pack(pady=10)
        # Cadre pour les boutons d'achat et de vente
        marche_frame = tk.Frame(self.village_info_frame, bg="#3A3A3A")
        marche_frame.pack(fill="x", pady=0)

        choix1 = tk.Button(marche_frame, text="Acheter", command=lambda: clique_acheter(), font=("Helvetica", 12, "bold"), bg="#2E2E2E", fg="white", activebackground="#2E2E2E", activeforeground="white", bd=0)
        choix1.pack(side="left", fill="x", expand=True)
        choix2 = tk.Button(marche_frame, text="Vendre", command=lambda: clique_vendre(), font=("Helvetica", 12, "bold"), bg="#3A3A3A", fg="white", activebackground="#2E2E2E", activeforeground="white", bd=0)
        choix2.pack(side="left", fill="x", expand=True)
        clique_acheter()
        self.action_bouton_selectionnee = "marche"

        
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
            elif action == "acheter" or action == "vendre":
                self.marche_bouton.config(bg="#3498DB")
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
        self.marche_bouton.config(bg="#1C6E8C")

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
        self.sauvegarde = False
        if self.action_selectionnee != None:
            if self.action_selectionnee == "impot":
                if self.map.selected_villages != []:
                    self.afficher_tour_journal()
                    self.ajouter_evenement("Action exécutée: Impot")
                    impot = 0
                    impot = self.gamecontroller.joueur.percevoir_impot(self.map.selected_villages)
                    self.ajouter_evenement(f"Impôt perçu: {impot}\n")
  
                    #self.gamecontroller.appliquer_evenements(self.gamecontroller.joueur.village_noble.habitants)
                    self.finir_tour()
                else:
                    self.ajouter_evenement("Vous devez choisir un village")
            
            
            elif self.action_selectionnee == "paysan" or self.action_selectionnee == "roturier":
                if self.map.selected_villages != []:
                    for village in self.map.selected_villages:
                        immigration = Immigration(village.noble)
                        if self.gamecontroller.obtenir_nombre_total_personnes(self.gamecontroller.joueur) >= self.gamecontroller.joueur.capacite_habitants:
                            self.ajouter_evenement("Vous avez atteint votre capacité maximale d'habitants")
                            return
                        if self.action_selectionnee == "roturier":
                            if self.gamecontroller.joueur.argent < 10:
                                self.ajouter_evenement("Vous n'avez pas assez d'argent pour immigrer un roturier")
                                return
                            self.afficher_tour_journal()
                            self.ajouter_evenement("Action exécutée: Immigration\n")
                            immigration.immigrer("roturier")
                            self.ajouter_evenement("Roturier immigré\n")
                        elif self.action_selectionnee == "paysan":
                            if self.gamecontroller.joueur.argent < 5:
                                self.ajouter_evenement("Vous n'avez pas assez d'argent pour immigrer un paysan")
                                return
                            self.afficher_tour_journal()
                            self.ajouter_evenement("Action exécutée: Immigration\n")
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
                if self.gamecontroller.joueur.argent < 10 and self.action_selectionnee == "infanterie":
                    self.ajouter_evenement("Vous n'avez pas assez d'argent pour recruter un soldat")
                    return
                elif self.gamecontroller.joueur.argent < 15 and self.action_selectionnee == "cavalier":
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
            
            elif self.action_selectionnee in ["vendre", "acheter"]:
                if self.quantite_achete_vend == 0:
                    self.ajouter_evenement("Vous devez choisir une quantité")
                    return
                if self.action_selectionnee == "acheter":
                    self.afficher_tour_journal()
                    self.ajouter_evenement("Action exécutée: Acheter ressources\n")
                    self.gamecontroller.joueur.augmenter_ressources(int(self.quantite_achete_vend*1.2))
                    self.gamecontroller.joueur.diminuer_argent(int(self.quantite_achete_vend))
                    self.ajouter_evenement("Vous avez acheté "+str(int(self.quantite_achete_vend*1.2))+" ressources pour "+str(int(self.quantite_achete_vend))+" argent\n")
                    self.finir_tour()
                elif self.action_selectionnee == "vendre":
                    self.afficher_tour_journal()
                    self.ajouter_evenement("Action exécutée: Vendre ressources\n")
                    self.gamecontroller.joueur.diminuer_ressources(int(self.quantite_achete_vend))
                    self.gamecontroller.joueur.augmenter_argent(int(self.quantite_achete_vend*0.8))
                    self.ajouter_evenement("Vous avez vendu "+str(int(self.quantite_achete_vend))+" ressources pour "+str(int(self.quantite_achete_vend*0.8))+" argent\n")
                    self.finir_tour()
        else:
            if self.verifier_fin_partie() == False:
                self.afficher_tour_journal()
                self.finir_tour()
            else:
                pass
           
    def verifier_fin_partie(self):
        """
        Vérifie si le joueur a perdu (pas d'instance self.joueur).
        Si c'est le cas, désactive tous les widgets et affiche un message.
        """
        x="perdu"
        if isinstance(self.gamecontroller.joueur, Seigneur):
            x="gagné"
            for i in self.gamecontroller.nobles:
                if i.seigneur != self.gamecontroller.joueur:
                    x="perdu"
            
        if self.gamecontroller.joueur == None or x=="gagné":
            
            # Mettre un frame transparent pour ne plus pouvoir cliquer sur les éléments du jeu
            self.overlay_frame = tk.Frame(self.root,bg='')
            self.overlay_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            
            self.affiche_frame = tk.Frame(self.overlay_frame, bg="#2E2E2E")
            self.affiche_frame.place(relx=0, rely=0.31, relwidth=1, relheight=0.38)
            
            # Afficher un message indiquant que le joueur a perdu
            message_perdu = tk.Label(
                self.root,
                text=f"Vous avez {x} !",
                font=("Helvetica", 24, "bold"),
                fg="white",
                bg="#2E2E2E"  # Couleur de fond de la fenêtre
            )
            message_perdu.place(relx=0.5, rely=0.43, anchor="center")  # Centrer le message

            # Ajouter éventuellement un bouton pour quitter ou redémarrer
            quitter_bouton = tk.Button(
                self.root,
                text="Quitter",
                command=self.root.quit,
                font=("Helvetica", 14),
                bg="#1C6E8C",
                fg="white",
                activebackground="#145374",
                activeforeground="white",
                bd=0
            )
            quitter_bouton.place(relx=0.5, rely=0.57, anchor="center")  # Position en dessous du message
            #enlever le bind echap
            self.root.unbind("<Escape>") # Enlever le binding de la touche Escape
            #self.root.resizable(False, False)  # Désactiver la redimension de la fenêtre
            return True
        else:
            return False

    
    def finir_tour(self):
        """reset les actions selectionnées"""
        
        self.action_selectionnee = None
        self.action_bouton_selectionnee = None
        self.quantite_achete_vend = 0
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
        if self.verifier_fin_partie() == False:
            self.mettre_a_jour_infos()
            self.mettre_a_jour_infos_village(self.map.village_affiché)
            self.map.mettre_a_jour_bordures()
            self.map.dessiner_map_visible()
        else:
            pass
    