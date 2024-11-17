import random

class Evenement:
    """
    Classe de base pour un événement dans le jeu.
    """

    def __init__(self, nom: str, probabilite: float):
        self.nom = nom
        self.probabilite = probabilite  # Probabilité de l'événement (0 à 1)

    def se_produit(self):
        """
        Détermine si l'événement se produit en fonction de la probabilité.
        """
        return random.random() < self.probabilite

    def appliquer(self, personnage):
        """
        Applique l'effet de l'événement sur un personnage.
        Cette méthode sera redéfinie dans les sous-classes.
        """
        raise NotImplementedError("Cette méthode doit être implémentée par les sous-classes")
