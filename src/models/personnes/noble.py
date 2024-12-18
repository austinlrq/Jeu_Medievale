from .personne import Personne
from .roturier import Roturier
from .soldat import Soldat
from src.views import Case

from typing import List

class Noble(Personne):
    """
    Classe représentant un noble, ayant des roturiers comme sujets.
    """
    from src.views import Case

    def __init__(self, nom: str, age: int, ressources: int, argent: int, bonheur: int, couleur_bordure="#FFFFFF", capacite_habitants=10, capacite_soldats=5):
        super().__init__(nom, age, ressources, argent, bonheur)
        self.couleur_bordure = couleur_bordure  # Couleur unique pour le seigneur
        self.village_noble = None
        self.armee: List[Soldat] = []  # Liste des soldats appartenant au Noble
        self.seigneur = None  # Instance de Seigneur
        self.cases: List[Case] = []  # Liste des cases détenues par le Noble
        self.capacite_habitants = capacite_habitants  # Nombre maximum d'habitants dans le village
        self.capacite_soldats = capacite_soldats  # Nombre maximum de soldats dans l'armée


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
            return total
        return 0

    def percevoir_impot(self, villages):
        """Collecte les impôts du village sous le contrôle du noble."""
        if self.village_noble:
            total_impots = self.village_noble.percevoir_impots()
            self.augmenter_ressources(total_impots)
            return total_impots
        return 0
    
    def recruter(self, soldat):
        """Recrute un soldat pour l'armée du noble."""
        self.armee.append(soldat)
        if soldat.type_soldat == "infanterie":
            self.diminuer_argent(10)
        elif soldat.type_soldat == "cavalier":
            self.diminuer_argent(15)
        print(f"{self.nom} a recruté {soldat.nom} dans son armée.")
    
    def ajouter_case(self, case):
        """Permet au noble d'acheter une case."""
        self.cases.append(case)  # Ajouter la case à la liste des cases détenues
            
    def devenir_seigneur(self, noble_vassalisé):
        from .seigneur import Seigneur
        """Transforme le noble en seigneur et promeut un nouvel habitant au rang de noble."""
        plus_riche = self.village_noble.trouver_plus_riche()
        if plus_riche:
            # Crée un nouveau noble pour le plus riche habitant
            nouveau_noble = Noble(plus_riche.nom, plus_riche.age, plus_riche.ressources, plus_riche.argent, plus_riche.bonheur)
            nouveau_noble.village_noble = self.village_noble  # Transfert du village au nouveau noble
            self.village_noble.habitants.remove(plus_riche)  # Retire le plus riche des habitants

            # Retourne une instance de Seigneur avec le village géré par le nouveau noble
            seigneur = Seigneur("seigneur", self.age, self.ressources, self.argent, self.bonheur, self.couleur_bordure, self.capacite_habitants, self.capacite_soldats)
            seigneur.vassaux.append(nouveau_noble)
            seigneur.vassaux.append(noble_vassalisé)
            seigneur.cases = self.cases
            seigneur.capacite_habitants += noble_vassalisé.capacite_habitants
            seigneur.capacite_soldats += noble_vassalisé.capacite_soldats
            nouveau_noble.seigneur = seigneur
            nouveau_noble.village_noble = self.village_noble
            nouveau_noble.cases = []
            noble_vassalisé.seigneur = seigneur
            noble_vassalisé.capacité_habitants = 0
            noble_vassalisé.capacité_soldats = 0
            for case in seigneur.cases:
                case.proprietaire = seigneur
            print(noble_vassalisé.cases)
            # Transfert des cases du noble vassalisé au seigneur
            for case in noble_vassalisé.cases:
                seigneur.ajouter_case(case)
                case.proprietaire = seigneur
            noble_vassalisé.cases.clear()
            print(seigneur.cases)

            print(f"{self.nom} devient seigneur, et {plus_riche.nom} devient noble et gère le village.")
            return seigneur, nouveau_noble
        else:
            print("Pas d'habitants disponibles pour devenir noble.")
            return None
        
    def devenir_seigneur_contre_seigneur(self, seigneur):
        from .seigneur import Seigneur
        print(len(seigneur.vassaux))
        nouv_seigneur = Seigneur("seigneur", self.age, self.ressources, self.argent, self.bonheur, self.couleur_bordure, self.capacite_habitants, self.capacite_soldats)
        nouv_seigneur.capacite_habitants += seigneur.capacite_habitants
        nouv_seigneur.capacite_soldats += seigneur.capacite_soldats
        for noble in seigneur.vassaux:
            nouv_seigneur.ajouter_vassal(noble)
        for case in seigneur.cases:
            case.proprietaire = nouv_seigneur
            nouv_seigneur.ajouter_case(case)
        for case in self.cases:
            case.proprietaire = nouv_seigneur
            nouv_seigneur.ajouter_case(case)
        seigneur.vassaux.clear()
        seigneur.cases.clear()
        # creer une nouvelle instance de noble pour le seigneur battu
        nouveau_noble = Noble(seigneur.nom, seigneur.age, seigneur.ressources, seigneur.argent, seigneur.bonheur, seigneur.couleur_bordure, 0, 0)
        nouveau_noble.seigneur = nouv_seigneur
        nouveau_noble.village_noble = self.village_noble
        nouveau_noble.village_noble.proprietaire = nouveau_noble
        nouv_seigneur.ajouter_vassal(nouveau_noble)
        print(len(nouv_seigneur.cases))
        return nouv_seigneur, nouveau_noble
        
        




    def possede_case_adjacente(self, case):
        """Vérifie si le joueur possède une case adjacente à la case donnée."""
        adjacentes = [
            (case.row - 1, case.col),  # Haut
            (case.row + 1, case.col),  # Bas
            (case.row, case.col - 1),  # Gauche
            (case.row, case.col + 1)   # Droite
        ]
        for adj in adjacentes:
            for c in self.cases:
                if c.row == adj[0] and c.col == adj[1]:
                    return True
        return False

    def __str__(self):
        return (
            super().__str__() +
            f", Type : Noble, "
            f" Village : {self.village_noble}"
            f", Armée : {self.armee}"
            f", Cases : {self.cases}"
            f", Seigneur : {self.seigneur}"
            f", Couleur bordure : {self.couleur_bordure}"
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
            "village_id": self.village_noble.id if self.village_noble else None,
            "armee": [soldat.to_dict() for soldat in self.armee],
            "seigneur": self.seigneur.nom if self.seigneur else None
        }