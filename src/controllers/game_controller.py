from src.models import Evenement
from src.models import RecolteAbondante
from src.models import Epidemie
from src.models import Immigration
 
# from src.models import GuerreCaracteristique
import random
from typing import List
from src.models import *

class GameController:
    def __init__(self):
        self.tour = 1
        self.couleurs_possibles = ["#0000FF",  # Bleu
                            "#800080",  # Violet
                            "#FFA500",  # Orange
                            "#FFFFFF"]  # Blanc
        self.villages, self.nobles = self.creer_villages(2, 3)
        self.seigneurs = []
        self.joueur = self.nobles[0]
        # Afficher le statut de chaque village
        for village in self.villages:
            village.afficher_statut()
        self.joueur.augmenter_argent(1000)
        

        """self.roturier1 = Roturier("Roturier 1", 20, 10, 10, 10, 5)
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
        self.immigration_action = Immigration(self.joueur)
        self.immigration_action.immigrer("roturier")
        self.seigneur = self.joueur.devenir_seigneur()
        
        self.seigneur.__str__()
        # Afficher le statut du village
        self.village_joueur.afficher_statut()"""

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


    # Création de plusieurs villages
    def creer_villages(self, n, habitants_par_village):
        villages = []
        nobles = []
        for i in range(n):
            nom_village = f"Village_{i}"
            village = Village(nom_village)
            
            # Création d'un noble pour chaque village
            noble = Noble(f"Noble_{i}", 30, 100, 50, 5, self.couleurs_possibles[i])
            noble.ajouter_village(village)
            village.ajouter_noble(noble)
            # Ajouter le noble comme gestionnaire du village
            #village.ajouter_habitant(noble)

            # Ajouter des habitants (paysans et roturiers) au village
            for j in range(habitants_par_village):
                if j % 2 == 0:
                    paysan = Paysan(f"Paysan_{i}_{j}", 20, 10, 15, 5)
                    village.ajouter_habitant(paysan)
                else:
                    roturier = Roturier(f"Roturier_{i}_{j}", 25, 15, 10, 10, 5)
                    village.ajouter_habitant(roturier)
            
            # Ajouter le village à la liste des villages
            villages.append(village)
            nobles.append(noble)
            print(f"{nom_village} a été créé avec un noble et des habitants.")

        return villages, nobles
    
    def obtenir_villages_joueur(self,joueur):
        """
        Retourne une liste des villages selon le type du joueur.
        - Si le joueur est noble, retourne son village.
        - Si le joueur est seigneur, retourne les villages de ses nobles.
        """
        if isinstance(joueur, Noble) and not isinstance(joueur, Seigneur):
            # Le joueur est un noble mais pas un seigneur
            return [joueur.village_noble]

        elif isinstance(joueur, Seigneur):
            # Le joueur est un seigneur, retourner les villages des nobles vassaux
            return [noble.village_noble for noble in joueur.vassaux if noble.village_noble]

        return []  # Retourne une liste vide si le joueur n'a pas de villages

    def obtenir_nombre_total_personnes(self, joueur):
        """
        Retourne le nombre total de personnes sous l'influence d'un joueur.
        - Si le joueur est noble, retourne la population de son village.
        - Si le joueur est seigneur, retourne la somme des populations des villages de ses nobles.
        """
        total_personnes = 0

        if isinstance(joueur, Noble) and not isinstance(joueur, Seigneur):
            # Le joueur est un noble mais pas un seigneur
            if joueur.village_noble:
                total_personnes += joueur.village_noble.population

        elif isinstance(joueur, Seigneur):
            # Le joueur est un seigneur, ajouter les populations des villages de ses nobles
            for noble in joueur.vassaux:
                if noble.village_noble:
                    total_personnes += noble.village_noble.population

        return total_personnes

    def guerre(self, attaquant, defenseur):
        """
        Simule une guerre entre deux armées : l'attaquant et le défenseur.
        Les deux sont des Nobles ou des Seigneurs avec des armées.

        :param attaquant: Noble ou Seigneur lançant l'attaque.
        :param defenseur: Noble ou Seigneur défendant son territoire.
        :return: Résultat de la guerre sous forme de texte.
        """
        # Calculer les forces totales des deux armées
        force_attaquante = sum(soldat.force for soldat in attaquant.armee)
        force_defensive = sum(soldat.force for soldat in defenseur.armee)

        print(f"L'armée de {attaquant.nom} attaque celle de {defenseur.nom} !")
        print(f"Force attaquante : {force_attaquante}")
        print(f"Force défensive : {force_defensive}")

        # Déterminer le gagnant
        if force_attaquante > force_defensive:
            pertes = int(force_defensive / 2)  # L'attaquant subit des pertes équivalentes à la moitié de la force défensive
            attaquant.armee = attaquant.armee[:len(attaquant.armee) - pertes]
            defenseur.armee = []  # Défenseur perd toute son armée
            print(f"{attaquant.nom} remporte la guerre contre {defenseur.nom} !")
            if isinstance(attaquant,Noble) and isinstance(defenseur,Noble):
                nouv_attaquant = attaquant.devenir_seigneur(defenseur)
                self.seigneurs.append(nouv_attaquant)
                self.nobles.remove(attaquant)
                print(nouv_attaquant)
                return nouv_attaquant
            if isinstance(attaquant,Seigneur) and isinstance(defenseur,Noble):
                return
                #return f"{attaquant.nom} a gagné et {defenseur.nom} a perdu toute son armée."

        elif force_attaquante < force_defensive:
            pertes = int(force_attaquante / 2)  # Le défenseur subit des pertes équivalentes à la moitié de la force attaquante
            defenseur.armee = defenseur.armee[:len(defenseur.armee) - pertes]
            attaquant.armee = []  # Attaquant perd toute son armée
            print(f"{defenseur.nom} défend avec succès contre {attaquant.nom} !")
            self.seigneur = defenseur.devenir_seigneur(attaquant)
            self.seigneurs.append(self.seigneur)
            return f"{defenseur.nom} a gagné et {attaquant.nom} a perdu toute son armée."

        else:
            # En cas d'égalité, les deux armées s'annihilent
            attaquant.armee = []
            defenseur.armee = []
            print("Les deux armées se sont annihilées dans une guerre acharnée !")
            return "Match nul : les deux armées ont été détruites."



    # def verifier_declenchement_guerre(self, seigneurs: List[Seigneur]):
    #     """Détermine si une guerre doit se déclencher entre deux seigneurs aléatoires."""
    #     if random.random() < 0.1:  # Exemple de probabilité de guerre
    #         attaquant = random.choice(seigneurs)
    #         defenseur = random.choice([s for s in seigneurs if s != attaquant])
    #         guerre = GuerreCaracteristique(attaquant, defenseur)
    #         self.guerres.append(guerre)
    #         guerre.declencher()  # Déclenche la guerre et applique les conséquences
