from src.models import Evenement
from src.models import RecolteAbondante
from src.models import Epidemie
# from src.models import GuerreCaracteristique
import random
from typing import List
from src.models import *

class GameController:
    def __init__(self):
        self.roturier1 = Roturier("Roturier 1", 20, 10, 10, 10, 5)
        self.roturier2 = Roturier("Roturier 2", 20, 10, 10, 10, 5)
        self.paysan1 = Paysan("Paysan 1", 20, 20, 15, 5)

        self.joueur = Noble("joueur", 20, 10, 10, 5)

        # Création du village
        self.village_joueur = Village("Village du Joueur")
        self.village_joueur.ajouter_habitant(self.roturier1)
        self.village_joueur.ajouter_habitant(self.roturier2)
        self.village_joueur.ajouter_habitant(self.paysan1)

        self.joueur.ajouter_village(self.village_joueur)

        #self.village_joueur.afficher_statut()
        # Calcul de la production et perception des impôts
        #self.village_joueur.produire_ressources()
        

        # Afficher le statut du village
        #self.village_joueur.afficher_statut()

        #self.village_joueur.afficher_statut()
        self.evenements = [
            RecolteAbondante(),
            Epidemie(),
            # Guerre()
        ]
    
    def appliquer_evenements(self, personnages):
        """
        Applique des événements aléatoires à une liste de personnages.
        """
        for evenement in self.evenements:
            for personnage in personnages:
                if evenement.se_produit():
                    evenement.appliquer(personnage)
    
    

    # def verifier_declenchement_guerre(self, seigneurs: List[Seigneur]):
    #     """Détermine si une guerre doit se déclencher entre deux seigneurs aléatoires."""
    #     if random.random() < 0.1:  # Exemple de probabilité de guerre
    #         attaquant = random.choice(seigneurs)
    #         defenseur = random.choice([s for s in seigneurs if s != attaquant])
    #         guerre = GuerreCaracteristique(attaquant, defenseur)
    #         self.guerres.append(guerre)
    #         guerre.declencher()  # Déclenche la guerre et applique les conséquences
