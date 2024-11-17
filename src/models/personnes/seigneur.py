from .noble import Noble
from typing import List

class Seigneur(Noble):
    """
    Classe représentant un seigneur, ayant des nobles comme vassaux.
    """

    def __init__(self, nom: str, age: int, ressources: int, argent: int, bonheur: int):
        super().__init__(nom, age, ressources, argent, bonheur)
        self.vassaux: List[Noble] = []

    def ajouter_vassal(self, vassal: Noble):
        """Ajoute un noble en tant que vassal de ce seigneur."""
        self.vassaux.append(vassal)

    def percevoir_impot(self):
        """
        Perçoit un impôt uniquement des nobles vassaux.
        """
        for vassal in self.vassaux:
            vassal_impots = int(vassal.ressources * 0.1)  # Le seigneur prend 50 % des ressources de chaque noble vassal
            vassal.diminuer_ressources(vassal_impots)
            self.augmenter_ressources(vassal_impots)

    def __str__(self):
        return (
            super().__str__() +
            f", Type : Seigneur, "
            f"Nombre de vassaux : {len(self.vassaux)}"
        )