from .personne import Personne
from .roturier import Roturier
from .soldat import Soldat

from typing import List

class Noble(Personne):
    """
    Classe représentant un noble, ayant des roturiers comme sujets.
    """

    def __init__(self, nom: str, age: int, ressources: int, argent: int, bonheur: int):
        super().__init__(nom, age, ressources, argent, bonheur)
        self.village_noble = None
        self.armee: List[Soldat] = []  # Liste des soldats appartenant au Noble

    def ajouter_village(self, village):
        """Ajoute un village au noble s'il n'en a pas déjà un."""
        if self.village_noble is None:
            self.village_noble = village
        else:
            print(f"{self.nom} a déjà un village et ne peut en ajouter un autre.")

    def produire_ressources(self):
        """Appelle la production dans le village sous le contrôle du noble."""
        if self.village_noble:
            total = self.village_noble.produire_ressources()
            self.augmenter_ressources(total)
            return total
        return 0

    def percevoir_impots(self):
        """Collecte les impôts du village sous le contrôle du noble."""
        if self.village_noble:
            total_impots = self.village_noble.percevoir_impots()
            self.augmenter_ressources(total_impots)
            return total_impots
        return 0
    
    def devenir_seigneur(self, noble_vassalisé):
        from .seigneur import Seigneur
        """Transforme le noble en seigneur et promeut un nouvel habitant au rang de noble."""
        plus_riche = self.village_noble.trouver_plus_riche()
        if plus_riche:
            # Crée un nouveau noble pour le plus riche habitant
            nouveau_noble = Noble(plus_riche.nom, plus_riche.age, plus_riche.ressources, plus_riche.argent, plus_riche.bonheur)
            nouveau_noble.village_noble = self.village_noble  # Transfert du village au nouveau noble
            self.village_noble.habitants.remove(plus_riche)  # Retire le plus riche des habitants
            #self.vassaux.append(nouveau_noble)  # Ajoute le nouveau noble comme vassal

            # Retourne une instance de Seigneur avec le village géré par le nouveau noble
            seigneur = Seigneur(self.nom, self.age, self.ressources, self.argent, self.bonheur)
            seigneur.vassaux.append(nouveau_noble)
            seigneur.vassaux.append(noble_vassalisé)
            print(f"{self.nom} devient seigneur, et {plus_riche.nom} devient noble et gère le village.")
            return seigneur
        else:
            print("Pas d'habitants disponibles pour devenir noble.")
            return None

    def __str__(self):
        return (
            super().__str__() +
            f", Type : Noble, "
            f"Village : {self.village_noble}"
        )