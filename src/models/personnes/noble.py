from .personne import Personne
from .roturier import Roturier
from typing import List

class Noble(Personne):
    """
    Classe représentant un noble, ayant des roturiers comme sujets.
    """

    def __init__(self, nom: str, age: int, ressources: int, argent: int, bonheur: int, couleur: str = "green"):
        super().__init__(nom, age, ressources, argent, bonheur)
        self.villages = []
        self.couleur = couleur

    def ajouter_village(self, village):
        self.villages.append(village)

    def produire_ressources(self):
        """Appelle la production dans chaque village sous le contrôle du noble."""
        total = 0
        for village in self.villages:
            total += village.produire_ressources()
        self.augmenter_ressources()

    def percevoir_impots(self):
        """Collecte les impôts de chaque village sous le contrôle du noble."""
        total_impots = sum(village.percevoir_impots() for village in self.villages)
        self.ressources += total_impots
        return total_impots

    def __str__(self):
        return (
            super().__str__() +
            f", Type : Noble, "
            f"Nombre de roturiers : {len(self.roturiers)}"
        )