from .noble import Noble
from typing import List
from .soldat import Soldat
from src.views import Case


class Seigneur(Noble):
    """
    Classe représentant un seigneur, ayant des nobles comme vassaux.
    """

    def __init__(self, nom: str, age: int, ressources: int, argent: int, bonheur: int, couleur_bordure="#FFFFFF"):
        super().__init__(nom, age, ressources, argent, bonheur)
        self.couleur_bordure = couleur_bordure  # Couleur unique pour le seigneur
        self.vassaux: List[Noble] = []
        self.armee: List[Soldat] = []  # Liste des soldats dans l'armée du Seigneur
        self.cases: List[Case] = []  # Liste des cases détenues par le Noble


    def ajouter_vassal(self, vassal: Noble):
        """Ajoute un noble en tant que vassal de ce seigneur."""
        self.vassaux.append(vassal)

        # Transfert des cases du noble vassalisé au seigneur
        for case in vassal.cases:
            self.ajouter_case(case)
            case.proprietaire = self
        vassal.cases.clear()
        vassal.seigneur = self

    def produire_ressources(self):
        total = 0
        for noble in self.vassaux:
            total += noble.produire_ressources()
        return total

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