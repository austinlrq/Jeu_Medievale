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
        self.interface = None
        self.tour = 1
        self.couleurs_possibles = ["#0000FF",  # Bleu
                            "#800080",  # Violet
                            "#FFA500",  # Orange
                            "#FFFFFF"]  # Blanc
        self.villages, self.nobles = self.creer_villages(4, 3)
        self.seigneurs = []
        self.seigneurs_vassalisés = []
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
    
    def set_interface(self, interface):
        self.interface = interface

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
    
    def construire(self, joueur, case, type_batiment):
        """
        Permet de construire une habitation dans un village.
        """
        if type_batiment == "habitation":
            if joueur.argent >= 10:
                joueur.diminuer_argent(10)
                joueur.capacite_habitants += 5
                case.batiment = type_batiment
                self.interface.ajouter_evenement(f"{joueur.nom} a construit une habitation dans le village.\n")
            else:
                self.interface.ajouter_evenement(f"{joueur.nom} n'a pas assez d'argent pour construire une habitation.\n")
                return False
        elif type_batiment == "camp":
            if joueur.argent >= 10:
                joueur.diminuer_argent(10)
                joueur.capacite_soldats += 5
                case.batiment = type_batiment
                self.interface.ajouter_evenement(f"{joueur.nom} a construit un camp d'entraînement dans le village.\n")
            else:
                self.interface.ajouter_evenement(f"{joueur.nom} n'a pas assez d'argent pour construire un camp d'entraînement.\n")
                return False

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
            self.interface.ajouter_evenement(f"L'attaquant remporte la guerre contre le defenseur !\n")
            if isinstance(attaquant,Seigneur) and isinstance(defenseur,Seigneur):
                attaquant.ajouter_vassal_seigneur(defenseur)
                self.seigneurs_vassalisés.append(defenseur)
            elif isinstance(attaquant,Seigneur) and isinstance(defenseur,Noble):
                attaquant.ajouter_vassal(defenseur)
            elif isinstance(attaquant,Noble) and isinstance(defenseur,Seigneur):
                nouv_attaquant, nouv_defenseur = attaquant.devenir_seigneur_contre_seigneur(defenseur)
                self.seigneurs.append(nouv_attaquant)
                self.seigneurs_vassalisés.append(nouv_defenseur)
                self.nobles.remove(attaquant)
                self.seigneurs.remove(defenseur)
                if self.joueur == attaquant:
                    self.joueur = nouv_attaquant
            elif isinstance(attaquant,Noble) and isinstance(defenseur,Noble):
                nouv_attaquant, nouv_defenseur = attaquant.devenir_seigneur(defenseur)
                self.seigneurs.append(nouv_attaquant)
                self.nobles.remove(attaquant)
                self.nobles.append(nouv_defenseur)
                if self.joueur == attaquant:
                    self.joueur = nouv_attaquant
        elif force_attaquante < force_defensive:
            pertes = int(force_attaquante / 2)  # Le défenseur subit des pertes équivalentes à la moitié de la force attaquante
            defenseur.armee = defenseur.armee[:len(defenseur.armee) - pertes]
            attaquant.armee = []  # Attaquant perd toute son armée
            self.interface.ajouter_evenement(f"Le defenseur défend avec succès contre l'attaquant !\n")
            if isinstance(defenseur,Seigneur) and isinstance(attaquant,Seigneur):
                defenseur.ajouter_vassal_seigneur(attaquant)
                self.seigneurs_vassalisés.append(attaquant)
            elif isinstance(defenseur,Seigneur) and isinstance(attaquant,Noble):
                defenseur.ajouter_vassal(attaquant)
            elif isinstance(defenseur,Noble) and isinstance(attaquant,Seigneur):
                nouv_defenseur, nouv_attaquant = defenseur.devenir_seigneur_contre_seigneur(attaquant)
                self.seigneurs.append(nouv_defenseur)
                self.seigneurs_vassalisés.append(nouv_attaquant)
                self.nobles.remove(defenseur)
                self.seigneurs.remove(attaquant)
                if self.joueur == attaquant:
                    self.joueur = nouv_defenseur
            elif isinstance(defenseur,Noble) and isinstance(attaquant,Noble):
                nouv_defenseur, nouv_attaquant = defenseur.devenir_seigneur(attaquant)
                self.seigneurs.append(nouv_defenseur)
                self.nobles.remove(attaquant)
                self.nobles.append(nouv_attaquant)
                if self.joueur == attaquant:
                    self.joueur = nouv_defenseur
        else:
            # En cas d'égalité, les deux armées s'annihilent
            attaquant.armee = []
            defenseur.armee = []
            self.interface.ajouter_evenement("Match nul : les deux armées ont été détruites.\n")
        
    def tour_suivant(self):
        """Passe au tour suivant et applique les événements aléatoires."""

        """if self.tour == 1:
            print("cases:",self.joueur.cases)
            print("cases:",self.nobles[1].cases)
            #tester tous les scenrios de guerre
            self.nobles[1].recruter(Soldat("Soldat 1", 10, "infanterie"))
            self.guerre(self.nobles[1],self.nobles[2])
            print("seigneur:",self.nobles[2].seigneur)
            print("seigneur:",self.nobles[1].seigneur)

        if self.tour == 4:
            self.seigneurs[0].recruter(Soldat("Soldat 2", 20, "infanterie"))
            self.guerre(self.seigneurs[0],self.seigneurs[1])
            print("seigneur:",self.nobles[0].seigneur)
            print("seigneur:",self.seigneurs[0].seigneur)"""

        self.tour += 1
        #self.appliquer_evenements(self.nobles)
        #self.appliquer_evenements(self.seigneurs)
        #self.verifier_declenchement_guerre(self.seigneurs)
        #self.verifier_declenchement_guerre(self.nobles)
        """for village in self.villages:
            village.afficher_statut()
        for noble in self.nobles:
            noble.__str__()
        for seigneur in self.seigneurs:
            seigneur.__str__()"""
        #produire les ressources de tous les personnages
        for seigneur in self.seigneurs:
            total = seigneur.produire_ressources()
            if seigneur.ressources < len(seigneur.armee)*2:
                seigneur.armee.pop(0)
                if seigneur==self.joueur:
                    self.interface.ajouter_evenement(f"Le village n'a pas assez de ressources pour l'armée.\n")
                    self.interface.ajouter_evenement(f"Un soldat est mort de faim.\n")
            else:
                seigneur.diminuer_ressources(len(seigneur.armee)*2)
                if seigneur==self.joueur:
                    self.interface.ajouter_evenement(f"Le village a dépensé {len(seigneur.armee)*2} ressources pour l'armée.\n")
            if seigneur==self.joueur:
                self.interface.ajouter_evenement(f"Le village a produit {total} ressources.\n")
            
        for noble in self.nobles:
            if noble.seigneur==None:
                total = noble.produire_ressources()
                if noble.ressources < len(noble.armee)*2:
                    noble.armee.pop(0)
                    if noble==self.joueur:
                        self.interface.ajouter_evenement(f"Le village n'a pas assez de ressources pour l'armée.\n")
                        self.interface.ajouter_evenement(f"Un soldat est mort de faim.\n")
                else:
                    noble.diminuer_ressources(len(noble.armee)*2)
                    if noble==self.joueur:
                        self.interface.ajouter_evenement(f"Le village a dépensé {len(noble.armee)*2} ressources pour l'armée.\n")
                if noble==self.joueur:
                    self.interface.ajouter_evenement(f"Le village a produit {total} ressources.\n")
                


    # def verifier_declenchement_guerre(self, seigneurs: List[Seigneur]):
    #     """Détermine si une guerre doit se déclencher entre deux seigneurs aléatoires."""
    #     if random.random() < 0.1:  # Exemple de probabilité de guerre
    #         attaquant = random.choice(seigneurs)
    #         defenseur = random.choice([s for s in seigneurs if s != attaquant])
    #         guerre = GuerreCaracteristique(attaquant, defenseur)
    #         self.guerres.append(guerre)
    #         guerre.declencher()  # Déclenche la guerre et applique les conséquences
