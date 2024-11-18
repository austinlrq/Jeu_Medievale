class Guerre:
    def __init__(self, attaquant, defenseur):
        """
        Initialise une guerre entre deux parties.
        :param attaquant: Noble ou Seigneur lançant l'attaque.
        :param defenseur: Noble ou Seigneur défendant son territoire.
        """
        self.attaquant = attaquant
        self.defenseur = defenseur

    def calculer_force(self, armee):
        """
        Calcule la force totale d'une armée.
        :param armee: Liste de soldats.
        :return: Force totale de l'armée.
        """
        return sum(soldat.force for soldat in armee)

    def resolution(self):
        """
        Résout la guerre et retourne le résultat.
        :return: Résultat sous forme de texte.
        """
        force_attaquante = self.calculer_force(self.attaquant.armee)
        force_defensive = self.calculer_force(self.defenseur.armee)

        print(f"L'armée de {self.attaquant.nom} attaque celle de {self.defenseur.nom} !")
        print(f"Force attaquante : {force_attaquante}")
        print(f"Force défensive : {force_defensive}")

        if force_attaquante > force_defensive:
            pertes = int(force_defensive / 2)  # L'attaquant subit des pertes
            self.attaquant.armee = self.attaquant.armee[:len(self.attaquant.armee) - pertes]
            self.defenseur.armee = []  # Le défenseur perd toute son armée
            print(f"{self.attaquant.nom} remporte la guerre contre {self.defenseur.nom} !")
            return f"{self.attaquant.nom} a gagné la guerre."

        elif force_attaquante < force_defensive:
            pertes = int(force_attaquante / 2)  # Le défenseur subit des pertes
            self.defenseur.armee = self.defenseur.armee[:len(self.defenseur.armee) - pertes]
            self.attaquant.armee = []  # L'attaquant perd toute son armée
            print(f"{self.defenseur.nom} défend avec succès contre {self.attaquant.nom} !")
            return f"{self.defenseur.nom} a gagné la guerre."

        else:
            # En cas d'égalité, les deux armées s'annihilent
            self.attaquant.armee = []
            self.defenseur.armee = []
            print("Les deux armées se sont annihilées dans une guerre acharnée !")
            return "Match nul : les deux armées ont été détruites."
