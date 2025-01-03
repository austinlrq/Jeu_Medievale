from src.models import Evenement
from src.models import RecolteAbondante
from src.models import Epidemie
from src.models import Immigration
from src.views.TYPE import TYPE
from src.controllers.bot_controller import action_bots

# from src.models import GuerreCaracteristique
import random
import json
from typing import List
from src.models import *

class GameController:
    def __init__(self, villages=None, nobles = None, joueur = None, tour = 0):
        self.interface = None

        # Lire le fichier settings.json
        with open('src/settings.json', 'r') as f:
            settings = json.load(f)

        # Extraire la valeur de NB_VILLAGE
        NB_VILLAGE = settings.get('NB_VILLAGE', 4)  # Utiliser 4 comme valeur par défaut si NB_VILLAGE n'est pas défini
        self.couleurs_possibles = ["#0000FF",  # Bleu
                                   "#800080",  # Violet
                                   "#FFA500",  # Orange
                                   "#FFFFFF"]  # Blanc
        self.nom_couleurs = ["Bleu", "Violet", "Orange", "Blanc"]
        
        # Si un village est passé en paramètre, l'initialisation prend en compte ce village
        if villages:
            self.villages = villages # Remplacer par un village existant
            self.nobles = nobles
            self.tour = tour
            self.joueur = joueur
            
        else:
            self.villages, self.nobles = self.creer_villages(NB_VILLAGE, 3)  # Créer des villages par défaut
            self.joueur = self.nobles[0]  # Le premier noble est le joueur
            self.tour = 1
            #self.joueur.augmenter_argent(1000)

        self.seigneurs = []
        self.seigneurs_vassalisés = []

        # Afficher le statut de chaque village
        for village in self.villages:
            village.afficher_statut()
        

        # Liste des événements
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
            village = Village(i,nom_village)
            
            # Création d'un noble pour chaque village
            noble = Noble(self.nom_couleurs[i], 30, 100, 50, 5, self.couleurs_possibles[i])
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
                self.interface.ajouter_evenement(f"{joueur.nom} a construit un camp dans le village.\n")
            else:
                self.interface.ajouter_evenement(f"{joueur.nom} n'a pas assez d'argent pour construire un camp.\n")
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
            if isinstance(attaquant,Seigneur) and isinstance(defenseur,Seigneur):
                attaquant.ajouter_vassal_seigneur(defenseur)
                self.seigneurs_vassalisés.append(defenseur)
                self.seigneurs.remove(defenseur)
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
                elif self.joueur == defenseur:
                    self.joueur = None
            elif isinstance(attaquant,Noble) and isinstance(defenseur,Noble):
                nouv_attaquant, nouv_defenseur = attaquant.devenir_seigneur(defenseur)
                self.seigneurs.append(nouv_attaquant)
                self.nobles.append(nouv_defenseur)
                self.nobles.remove(attaquant)
                if self.joueur == attaquant:
                    self.joueur = nouv_attaquant
                if self.joueur == defenseur:
                    self.joueur = None
            self.interface.ajouter_evenement(f"L'attaquant remporte la guerre contre le defenseur !\n")
        elif force_attaquante < force_defensive:
            pertes = int(force_attaquante / 2)  # Le défenseur subit des pertes équivalentes à la moitié de la force attaquante
            defenseur.armee = defenseur.armee[:len(defenseur.armee) - pertes]
            attaquant.armee = []  # Attaquant perd toute son armée
            if isinstance(defenseur,Seigneur) and isinstance(attaquant,Seigneur):
                defenseur.ajouter_vassal_seigneur(attaquant)
                self.seigneurs_vassalisés.append(attaquant)
                self.seigneurs.remove(attaquant)
            elif isinstance(defenseur,Seigneur) and isinstance(attaquant,Noble):
                defenseur.ajouter_vassal(attaquant)
            elif isinstance(defenseur,Noble) and isinstance(attaquant,Seigneur):
                nouv_defenseur, nouv_attaquant = defenseur.devenir_seigneur_contre_seigneur(attaquant)
                self.seigneurs.append(nouv_defenseur)
                self.seigneurs_vassalisés.append(nouv_attaquant)
                self.nobles.remove(defenseur)
                self.seigneurs.remove(attaquant)
                if self.joueur == defenseur:
                    self.joueur = nouv_defenseur
                if self.joueur == attaquant:
                    self.joueur = None
            elif isinstance(defenseur,Noble) and isinstance(attaquant,Noble):
                if defenseur == self.joueur:
                    self.interface.ajouter_evenement(f"{attaquant.nom} vous a attaqué")
                nouv_defenseur, nouv_attaquant = defenseur.devenir_seigneur(attaquant)
                self.seigneurs.append(nouv_defenseur)
                self.nobles.remove(defenseur)
                self.nobles.append(nouv_attaquant)
                if self.joueur == defenseur:
                    self.joueur = nouv_defenseur
                if self.joueur == attaquant:
                    self.joueur = None
            self.interface.ajouter_evenement(f"Le defenseur défend avec succès contre l'attaquant !\n")

        else:
            # En cas d'égalité, les deux armées s'annihilent
            attaquant.armee = []
            defenseur.armee = []
            if defenseur == self.joueur:
                self.interface.ajouter_evenement(f"{attaquant.nom} vous a attaqué")
                self.interface.ajouter_evenement(f"Match nul : les deux armées ont été détruites.\n")
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
        
        for seigneur in self.seigneurs:
            total = seigneur.produire_ressources()
            if len(seigneur.armee) != 0:
                if seigneur.ressources < len(seigneur.armee)*2:
                    seigneur.armee.pop(0)
                    if seigneur==self.joueur:
                        self.interface.ajouter_evenement(f"Le village n'a pas assez de ressources pour l'armée.\n")
                        self.interface.ajouter_evenement(f"Un soldat est mort de faim.\n")
                else:
                    seigneur.diminuer_ressources(len(seigneur.armee)*2)
                    if seigneur==self.joueur:
                        self.interface.ajouter_evenement(f"Le village a dépensé {len(seigneur.armee)*2} ressources pour l'armée.\n")
            montagne,foret,eau=0,0,0
            for case in seigneur.cases:
                if case.type in [TYPE.montagne,TYPE.montagneclair]:
                    seigneur.augmenter_argent(5)
                    montagne+=5
                elif case.type in [TYPE.foret,TYPE.foretclair]:
                    seigneur.augmenter_ressources(4)
                    foret+=4
                elif case.type in [TYPE.eau,TYPE.eauclair]:
                    seigneur.augmenter_ressources(7)
                    eau+=7
            if seigneur==self.joueur:
                if total:
                    self.interface.ajouter_evenement(f"Le village a produit {total} ressources.\n")
                    if montagne:
                        self.interface.ajouter_evenement(f"Le village a produit {montagne} argent grace aux montagnes")
                    if foret:
                        self.interface.ajouter_evenement(f"Le village a produit {foret} ressources grace aux forets")
                    if eau:
                        self.interface.ajouter_evenement(f"Le village a produit {eau} ressources grace aux eaux\n")
            
        for noble in self.nobles:
            if noble.seigneur==None:
                total = noble.produire_ressources()
                if len(noble.armee) != 0:
                    if noble.ressources < len(noble.armee)*2:
                        noble.armee.pop(0)
                        if noble==self.joueur:
                            self.interface.ajouter_evenement(f"Le village n'a pas assez de ressources pour l'armée.\n")
                            self.interface.ajouter_evenement(f"Un soldat est mort de faim.\n")
                    else:
                        noble.diminuer_ressources(len(noble.armee)*2)
                        if noble==self.joueur:
                            self.interface.ajouter_evenement(f"Le village a dépensé {len(noble.armee)*2} ressources pour l'armée.\n")
                montagne,foret,eau=0,0,0
                for case in noble.cases:
                    if case.type in [TYPE.montagne,TYPE.montagneclair]:
                        noble.augmenter_argent(5)
                        montagne+=5
                    elif case.type in [TYPE.foret,TYPE.foretclair]:
                        noble.augmenter_ressources(4)
                        foret+=4
                    elif case.type in [TYPE.eau,TYPE.eauclair]:
                        noble.augmenter_ressources(7)
                        eau+=7
                if noble==self.joueur:
                    if total:
                        self.interface.ajouter_evenement(f"Le village a produit {total} ressources.\n")
                        if montagne:
                            self.interface.ajouter_evenement(f"Le village a produit {montagne} argent grace aux montagnes")
                        if foret:
                            self.interface.ajouter_evenement(f"Le village a produit {foret} ressources grace aux forets")
                        if eau:
                            self.interface.ajouter_evenement(f"Le village a produit {eau} ressources grace aux eaux\n")
        
        # action_bots(self)

        for village in self.villages:
            for habitant in village.habitants:
                if habitant.mort_aleatoire():
                    village.habitants.remove(habitant)
                    self.interface.ajouter_evenement(f"Un habitant est mort de vieillesse.\n")
                else:
                    habitant.vieillir()
                print(habitant.age)