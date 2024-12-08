class Case:
    def __init__(self, row, col, type="plaine", proprietaire=None, prix=10):
        """
        Initialise une case.
        :param row: Coordonnée de la ligne de la case.
        :param col: Coordonnée de la colonne de la case.
        :param proprietaire: proprietaire actuel de la case.
        :param prix: Prix de la case.
        """
        self.row = row
        self.col = col
        self.type = type
        self.proprietaire = proprietaire
        self.prix = prix
        self.batiment = None  # Aucun bâtiment par défaut
        self.village = None  # Aucun village par défaut

    def acheter(self, joueur):
        """
        Permet à un joueur d'acheter la case.
        """
        if self.proprietaire is None and joueur.argent >= self.prix:
            joueur.diminuer_argent(self.prix)
            joueur.ajouter_case(self)
            self.proprietaire = joueur
            print(f"Case ({self.row}, {self.col}) achetée par {joueur.nom} pour {self.prix}.")
        else:
            print("Achat impossible : Case déjà achetée ou fonds insuffisants.")

    def construire_batiment(self, type_batiment):
        """
        Permet de construire un bâtiment sur la case.
        :param type_batiment: Classe ou type de bâtiment à construire.
        """
        if self.batiment is None:
            self.batiment = type_batiment
            print(f"Bâtiment {type_batiment.nom} construit sur la case ({self.row}, {self.col}).")
        else:
            print(f"Impossible de construire : un bâtiment est déjà présent ({self.batiment.nom}).")
