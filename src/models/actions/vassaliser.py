import random
from src.models.personnes import Seigneur, Noble

class TentativeVassalisation:
    """
    Classe représentant une tentative de vassalisation dans le jeu.
    """

    def __init__(self, seigneur: Seigneur, cible: Noble, cause: str = "Extension de l'influence"):
        self.seigneur = seigneur
        self.cible = cible
        self.cause = cause
        self.resultat = None

    def tenter_vassalisation(self):
        """
        Tente de vassaliser la cible. Plus le seigneur a de ressources et d'argent par rapport à la cible,
        plus les chances de succès sont grandes.
        """
        chance_succes = self.calculer_chance_succes()
        tentative = random.uniform(0, 100)
        
        if tentative <= chance_succes:
            self.resultat = "succès"
            self.appliquer_consequences()
            print(f"{self.seigneur.nom} a réussi à vassaliser {self.cible.nom}.")
        else:
            self.resultat = "échec"
            print(f"{self.seigneur.nom} a échoué à vassaliser {self.cible.nom}.")

    def calculer_chance_succes(self):
        """
        Calcule les chances de succès de la vassalisation en fonction des ressources et de l'argent.
        """
        ratio_ressources = self.seigneur.ressources / max(1, self.cible.ressources)
        ratio_argent = self.seigneur.argent / max(1, self.cible.argent)
        
        # La probabilité de succès est influencée par les ratios de ressources et d'argent
        chance_succes = min(90, (ratio_ressources + ratio_argent) * 25)
        return chance_succes

    def appliquer_consequences(self):
        """
        Applique les conséquences de la vassalisation en ajoutant le noble à la liste des vassaux du seigneur.
        """
        self.seigneur.ajouter_vassal(self.cible)
        self.cible.bonheur -= 10  # Le bonheur du noble peut diminuer en cas de vassalisation forcée.
