from src.models import *
class Village:
    def __init__(self, id, nom, x = None, y = None):
        self.nom = nom
        self.habitants = []  # Liste d'instances de Roturier et de Paysan
        self.noble = None  # Instance de Noble
        self.x= x
        self.y = y
        self.id = id

    def get_coords(self):
        return (self.x, self.y)
    
    def ajouter_habitant(self, habitant):
        """Ajoute un habitant au village."""
        self.habitants.append(habitant)

    def ajouter_noble(self, noble):
        """Ajoute un noble au village."""
        self.noble = noble
    
    @property
    def population(self):
        return len(self.habitants)

    def produire_ressources(self):
        """Calcule la production totale des habitants."""
        production_totale = sum(habitant.produire() for habitant in self.habitants)
        print(f"Production totale dans {self.nom} : {production_totale}")
        return production_totale

    def percevoir_impots(self):
        """Calcule les impôts perçus en fonction du type d'habitant."""
        total_impots = 0
        for habitant in self.habitants:
            if isinstance(habitant, Paysan):
                impots = int(habitant.ressources * 0.5)  # 50% pour les paysans
            elif isinstance(habitant, Roturier):
                impots = int(habitant.ressources * 0.25)  # 25% pour les roturiers
            else:
                impots = 0
            habitant.diminuer_ressources(impots)  # Soustraire les impôts de la richesse de l'habitant
            total_impots += impots
        return total_impots

    def afficher_statut(self):
        """Affiche les informations générales et de chaque habitant."""
        print(f"Village {self.nom} - Population : {self.population}")
        for habitant in self.habitants:
            print(f"{habitant.nom} - Ressources : {habitant.ressources}, Richesse : {habitant.argent}, Bonheur : {habitant.bonheur}")
        print("")

    @property
    def total_ressources(self):
        total = 0
        for habitant in self.habitants:
            total += habitant.ressources
        return total
    
    @property
    def total_argent(self):
        total = 0
        for habitant in self.habitants:
            total += habitant.argent
        return total

    def trouver_plus_riche(self):
        """Retourne l'habitant le plus riche du village."""
        if not self.habitants:
            return None
        return max(self.habitants, key=lambda habitant: habitant.argent)

    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "habitant": [habitant.to_dict() for habitant in self.habitants],
            "noble": self.noble.to_dict()
        }