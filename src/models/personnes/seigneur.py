from .noble import Noble
from typing import List
from .soldat import Soldat
from src.views import Case


class Seigneur(Noble):
    """
    Classe représentant un seigneur, ayant des nobles comme vassaux.
    """

    def __init__(self, nom: str, age: int, ressources: int, argent: int, bonheur: int, couleur_bordure="#FFFFFF", capacite_habitants=10, capacite_soldats=5):
        super().__init__(nom, age, ressources, argent, bonheur)
        self.couleur_bordure = couleur_bordure  # Couleur unique pour le seigneur
        self.vassaux: List[Noble] = []
        self.armee: List[Soldat] = []  # Liste des soldats dans l'armée du Seigneur
        self.cases: List[Case] = []  # Liste des cases détenues par le Noble
        self.capacite_habitants = capacite_habitants  # Nombre maximum d'habitants dans le village
        self.capacite_soldats = capacite_soldats  # Nombre maximum de soldats dans l'armée


    def ajouter_vassal(self, vassal: Noble):
        """Ajoute un noble en tant que vassal de ce seigneur."""
        self.vassaux.append(vassal)
        self.capacite_habitants += vassal.capacite_habitants
        self.capacite_soldats += vassal.capacite_soldats
        vassal.capacite_habitants = 0
        vassal.capacite_soldats = 0
        # Transfert des cases du noble vassalisé au seigneur
        for case in vassal.cases:
            self.ajouter_case(case)
            case.proprietaire = self
        vassal.cases.clear()
        vassal.seigneur = self

    def ajouter_vassal_seigneur(self, seigneur: "Seigneur"):
        """Ajoute un seigneur en tant que vassal de ce seigneur."""
        self.capacite_habitants += seigneur.capacite_habitants
        self.capacite_soldats += seigneur.capacite_soldats
        seigneur.capacite_habitants = 0
        seigneur.capacite_soldats = 0
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
    
    def to_dict(self):
        return {
            "nom": self.nom,
            "age": self.age,
            "ressources": self.ressources,
            "argent": self.argent,
            "bonheur": self.bonheur,
            "couleur_bordure": self.couleur_bordure,
            "capacite_habitants": self.capacite_habitants,
            "capacite_soldats": self.capacite_soldats,
            "vassaux": [vassal.nom for vassal in self.vassaux], 
            "armee": [soldat.to_dict() for soldat in self.armee],  # Assure-toi que Soldat possède une méthode to_dict()
            "cases": [{"row": case.row, "col": case.col, "type": case.type} for case in self.cases],
        }