import tkinter as tk
from tkinter import font

class AideInterface:
    def __init__(self, root, frame):
        self.root = root
        self.title_font = font.Font(family="Helvetica", size=25, weight="bold")
        self.title2_font = font.Font(family="Helvetica", size=20, weight="bold")
        self.texte_font = font.Font(family="Helvetica", size=16)
        self.texte_font_souligné = font.Font(family="Helvetica", size=18, underline=True)
        self.frame = frame

    def afficher(self):
        """Affichage de l'interface d'aide."""
        # Cache l'ancien frame
        self.frame.pack_forget()
        # Création d'un nouveau frame
        self.frame_aide = tk.Frame(self.root, bg="#2E2E2E")
        self.frame_aide.pack(fill="both", expand=True)

        # Créer le canvas pour le contenu défilant
        self.canvas = tk.Canvas(self.frame_aide, bg="#2E2E2E")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Créer la scrollbar
        self.scrollbar = tk.Scrollbar(self.frame_aide, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        # Configurer le canvas pour utiliser la scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Créer un frame pour le contenu à l'intérieur du canvas
        self.scrollable_frame = tk.Frame(self.canvas, bg="#2E2E2E")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Lier l'événement de redimensionnement de la fenêtre
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        # Lier l'événement de la molette de la souris
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Ajouter le bouton "Retour"
        self.bouton_quitter = tk.Button(
            self.scrollable_frame, 
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
        self.title = tk.Label(self.scrollable_frame, text="Aide", font=self.title_font, bg="#2E2E2E", fg="#90EE90")
        self.title.pack(side="top", pady=10)

        # Regles du jeu
        self.title_regle = tk.Label(self.scrollable_frame, text="Règles du jeu", font=self.title2_font, bg="#2E2E2E", fg="#2D8FB0", justify="left")
        self.title_regle.pack(side="top", anchor="nw", padx=5, pady=10)
        self.texte_regle = tk.Label(
            self.scrollable_frame, font=self.texte_font, bg="#2E2E2E", fg="white", wraplength=800, justify="left",
            text="Le but du jeu est de devenir le seigneur le plus puissant de la région. Pour cela, vous devrez recruter des soldats, construire des bâtiments, et gérer vos ressources de manière efficace.\n"
        )
        self.texte_regle.pack(side="top", anchor="w", padx=35,pady=10)
        
        # Types de terrains
        self.title_terrains = tk.Label(self.scrollable_frame, text="Types de terrains", font=self.texte_font_souligné, bg="#2E2E2E", fg="white", justify="left")
        self.title_terrains.pack(side="top", anchor="nw", padx=35, pady=10)
        self.texte_terrains = tk.Label(self.scrollable_frame, font=self.texte_font, bg="#2E2E2E", fg="white", wraplength=800, justify="left",
        text=
        "Chaque case sur la carte correspond à un type de terrain, influençant vos choix stratégiques :\n\n"+
        "Plaine : Idéal pour les habitations et les camps militaires.\n"+
        "Montagne : Fournit 5 d'argent par tour par case possédée, les constructions sont impossibles.\n"+
        "Eau : Fournit 7 ressources par tour par case possédée, les constructions sont impossibles.\n"+
        "Forêt : Fournit 4 ressources par tour par case possédée, les constructions sont impossibles.\n"
        )
        self.texte_terrains.pack(side="top", anchor="w", padx=35,pady=10)
        
        # Types de bâtiments
        self.title_batiments = tk.Label(self.scrollable_frame, text="Types de bâtiments", font=self.texte_font_souligné, bg="#2E2E2E", fg="white", justify="left")
        self.title_batiments.pack(side="top", anchor="nw", padx=35, pady=10)
        self.texte_batiments = tk.Label(self.scrollable_frame, font=self.texte_font, bg="#2E2E2E", fg="white", wraplength=800, justify="left",
        text="Certains bâtiments peuvent être construits sur vos territoires pour améliorer vos capacités :\n\n"+
        "Habitation : Augmente la population maximale de votre village.\n"+
        "Camp militaire : Permet de recruter des soldats.\n"
        )
        self.texte_batiments.pack(side="top", anchor="w", padx=35,pady=10)
        
        # Population
        self.title_population = tk.Label(self.scrollable_frame, text="Population", font=self.texte_font_souligné, bg="#2E2E2E", fg="white", justify="left")
        self.title_population.pack(side="top", anchor="nw", padx=35, pady=10)
        self.texte_population = tk.Label(self.scrollable_frame, font=self.texte_font, bg="#2E2E2E", fg="white", wraplength=800, justify="left",
        text="Votre village est peuplé de trois types d’habitants, chacun ayant un rôle spécifique :\n\n"+
        "Paysans : Produisent des ressources pour votre village.\n"+
        "Roturiers : Produisent plus de ressources que les paysans.\n"+
        "Soldats : Protègent votre village des attaques ennemies.\n"
        )
        self.texte_population.pack(side="top", anchor="w", padx=35,pady=10)
        
        # Ressources
        self.title_ressources = tk.Label(self.scrollable_frame, text="Ressources", font=self.texte_font_souligné, bg="#2E2E2E", fg="white", justify="left")
        self.title_ressources.pack(side="top", anchor="nw", padx=35, pady=10)
        self.texte_ressources = tk.Label(self.scrollable_frame, font=self.texte_font, bg="#2E2E2E", fg="white", wraplength=800, justify="left",
        text="Les ressources sont au cœur de la gestion de votre village :\n\n"+
        "Argent : Utilisé pour recruter des habitants et construire des bâtiments.\n"+
        "Ressources : Utilisées pour nourrir vos soldats et votre population.\n"
        )
        self.texte_ressources.pack(side="top", anchor="w", padx=35,pady=10)
        
        #Actions disponibles
        self.title_actions = tk.Label(self.scrollable_frame, text="Actions disponibles", font=self.texte_font_souligné, bg="#2E2E2E", fg="white", justify="left")
        self.title_actions.pack(side="top", anchor="nw", padx=35, pady=10)
        self.texte_actions = tk.Label(self.scrollable_frame, font=self.texte_font, bg="#2E2E2E", fg="white", wraplength=800, justify="left",
        text="Les joueurs peuvent effectuer une action lors de leur tour :\n\n"+
        "Percevoir les impôts : Collectez l'argent des habitants pour financer vos projets.\n"+
        "Acheter et vendre des ressources : Ajustez vos stocks en fonction des besoins du village.\n"+
        "Recruter des soldats : Formez une armée pour protéger votre territoire ou attaquer.\n"+
        "Construire des bâtiments : Étendez votre village en construisant des habitats, des camps ou des entrepôts.\n"+
        "Déclarer la guerre : Envahissez les territoires ennemis pour étendre votre domaine.\n"
        )
        self.texte_actions.pack(side="top", anchor="w", padx=35,pady=10)
        
        #Guerre et conquête
        self.title_guerre = tk.Label(self.scrollable_frame, text="Guerre et conquête", font=self.texte_font_souligné, bg="#2E2E2E", fg="white", justify="left")
        self.title_guerre.pack(side="top", anchor="nw", padx=35, pady=10)
        self.texte_guerre = tk.Label(self.scrollable_frame, font=self.texte_font, bg="#2E2E2E", fg="white", wraplength=800, justify="left",
        text="La guerre est un élément clé du jeu, mais attention aux conséquences :\n\n"+
        "La guerre est une mécanique centrale pour conquérir de nouveaux territoires.\n"+
        "Vous ne pouvez attaquer qu’un noble ou seigneur adjacent à vos territoires.\n"+
        "La puissance militaire est déterminée par le nombre et le type de soldats.\n"+
        "Après une victoire, les territoires ennemis sont annexés à votre domaine.\n"+
        "Après une défaite, vous perdez.\n"
        )
        self.texte_guerre.pack(side="top", anchor="w", padx=35,pady=10)
        
        
        
        # Commandes
        self.title_commandes = tk.Label(self.scrollable_frame, text="Commandes", font=self.title2_font, bg="#2E2E2E", fg="#2D8FB0", justify="left")
        self.title_commandes.pack(side="top", anchor="nw", padx=5, pady=10)
        self.texte_commandes = tk.Label(
            self.scrollable_frame, font=self.texte_font, bg="#2E2E2E", fg="white", wraplength=800, justify="left",
            text=
            "Ctrl + Clique gauche : sur un village pour afficher ses informations\n\n"+
            "Maintenir Clique droit : sur la carte pour se deplacer\n\n"+
            "Molette avant/arrière : sur la carte pour zoomer/dezoomer\n\n"+
            "Echap : pour afficher le menu pause\n\n"+
            "Espace : pour centrer la carte sur le village du joueur\n\n"
        )
        self.texte_commandes.pack(side="top", anchor="w", padx=35,pady=10)
        
        # Credits
        self.title_credits = tk.Label(self.scrollable_frame, text="Crédits", font=self.title2_font, bg="#2E2E2E", fg="#2D8FB0", justify="left")
        self.title_credits.pack(side="top", anchor="nw", padx=5, pady=10)
        self.texte_credits = tk.Label(
            self.scrollable_frame, font=self.texte_font, bg="#2E2E2E", fg="white", wraplength=800, justify="left",
            text="Développé par : \n\n"+
            "    - Austin L. \n"+
            "    - Joshua D. \n\n"+
            "Dans le cadre du projet de fin de semestre de la licence informatique de l'Université de Toulon.\n"
        )
        self.texte_credits.pack(side="top", anchor="w", padx=35,pady=10)
        
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        
        
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def on_canvas_configure(self, event):
        # Ajuster la taille de scrollable_frame pour qu'il prenne toute la place dans le canvas
        self.canvas.itemconfig(self.window_id,  width=event.width)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.scrollbar.lift(self.canvas)
        self.texte_regle.config(wraplength=event.width-70)
        self.texte_terrains.config(wraplength=event.width-70)
        self.texte_batiments.config(wraplength=event.width-70)
        self.texte_population.config(wraplength=event.width-70)
        self.texte_ressources.config(wraplength=event.width-70)
        self.texte_actions.config(wraplength=event.width-70)
        self.texte_guerre.config(wraplength=event.width-70)
        self.texte_commandes.config(wraplength=event.width-70)
        self.texte_credits.config(wraplength=event.width-70)
        
    def quitter(self):
        """Retour au menu principal."""
        self.frame_aide.pack_forget()
        self.frame.pack(fill="both", expand=True)