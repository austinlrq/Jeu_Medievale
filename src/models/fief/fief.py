class Fief:
    def __init__(self, nom, seigneur):
        self.nom = nom
        self.seigneur = seigneur
        self.villages = []

    def ajouter_village(self, village):
        """Ajoute un village au fief."""
        self.villages.append(village)
        print(f"{village.nom} a été ajouté au fief {self.nom}.")

    def percevoir_impots_fief(self):
        """Calcule les impôts perçus dans tout le fief."""
        total_impots = sum(village.percevoir_impots() for village in self.villages)
        self.seigneur.ressources += total_impots
        return total_impots

    def production_totale(self):
        """Calcule la production totale de ressources de tous les villages du fief."""
        return sum(village.produire_ressources() for village in self.villages)

    def afficher_statut(self):
        """Affiche l'état du fief et de ses villages."""
        print(f"Fief {self.nom} contrôlé par {self.seigneur.nom}")
        for village in self.villages:
            village.afficher_statut()
