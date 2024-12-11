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
        self.capacite_habitants = 10  # Nombre maximum d'habitants dans le village
        self.capacite_soldats = 5  # Nombre maximum de soldats dans l'armée


    def ajouter_vassal(self, vassal: Noble):
        """Ajoute un noble en tant que vassal de ce seigneur."""
        self.vassaux.append(vassal)

        # Transfert des cases du noble vassalisé au seigneur
        for case in vassal.cases:
            self.ajouter_case(case)
            case.proprietaire = self
        vassal.cases.clear()
        vassal.seigneur = self

    def ajouter_vassal_seigneur(self, seigneur: "Seigneur"):
        """Ajoute un seigneur en tant que vassal de ce seigneur."""
        for vassal in seigneur.vassaux:
            self.ajouter_vassal(vassal)
        for case in seigneur.cases:
            self.ajouter_case(case)
            case.proprietaire = self
        seigneur.vassaux.clear()
        seigneur.cases.clear()

    def produire_ressources(self):
        total = 0
        for noble in self.vassaux:
            total += noble.produire_ressources()
        return total

    def percevoir_impot(self, villages):
        """
        Perçoit un impôt uniquement des nobles vassaux.
        """
        from src.models import Village
        from src.models import Noble
        total_impots = 0
        for village in villages:
            village.noble.percevoir_impot(village)
            vassal_impots = int(village.noble.ressources * 0.1)  # Le seigneur prend 50 % des ressources de chaque noble vassal
            village.noble.diminuer_ressources(vassal_impots)
            self.augmenter_ressources(vassal_impots)
            total_impots += vassal_impots
        return total_impots


    def __str__(self):
        return (
            super().__str__() +
            f", Type : Seigneur, "
            f"Nombre de vassaux : {len(self.vassaux)}"
        )