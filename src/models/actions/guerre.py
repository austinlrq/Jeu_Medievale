import random
from typing import List
from src.models.personnes import Seigneur, Noble

class Guerre:
    """
    Classe représentant une guerre dans le jeu.
    """

    def __init__(self, attaquant: Seigneur, defenseur: Seigneur, cause: str = "Conflit de territoire"):
        self.attaquant = attaquant
        self.defenseur = defenseur
        self.cause = cause
        self.resultat = None

    def declencher(self):
        """Déclenche la guerre et détermine le vainqueur."""
        puissance_attaquant = self.calculer_puissance(self.attaquant)
        puissance_defenseur = self.calculer_puissance(self.defenseur)
        
        # Calculer le vainqueur en fonction de la puissance
        if puissance_attaquant > puissance_defenseur:
            self.resultat = "attaquant"
            self.appliquer_consequences(self.attaquant, self.defenseur)
        elif puissance_defenseur > puissance_attaquant:
            self.resultat = "defenseur"
            self.appliquer_consequences(self.defenseur, self.attaquant)
        else:
            self.resultat = "egalite"
            print("La guerre se termine en égalité.")

    def calculer_puissance(self, seigneur: Seigneur):
        """Calcule la puissance de guerre d'un seigneur en fonction de ses ressources et de ses vassaux."""
        puissance = seigneur.ressources + sum(vassal.ressources for vassal in seigneur.vassaux)
        return puissance

    def appliquer_consequences(self, vainqueur: Seigneur, perdant: Seigneur):
        """Applique les conséquences de la guerre aux seigneurs et leurs ressources."""
        # Transfert de ressources ou pertes
        perte_ressources = random.randint(10, 50)
        transfert_ressources = random.randint(20, 100)

        perdant.ressources = max(0, perdant.ressources - perte_ressources)
        vainqueur.ressources += transfert_ressources
        
        print(f"{vainqueur.nom} remporte la guerre contre {perdant.nom} et gagne {transfert_ressources} ressources.")
        print(f"{perdant.nom} perd {perte_ressources} ressources en conséquence de la défaite.")