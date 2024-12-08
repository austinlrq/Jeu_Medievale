from .personne import Personne

class Roturier(Personne):
    """
    Classe représentant un roturier, un type de personne dans la société médiévale.
    """

    def __init__(self, nom: str, age: int, ressources: int, argent: int, capacite_production: int, bonheur: int):
        super().__init__(nom, age, ressources, argent, bonheur)
        self.capacite_production = capacite_production

    def produire(self):
        """Augmente les ressources en fonction de la capacité de production."""
        self.augmenter_ressources(self.capacite_production)
        return self.capacite_production

    def __str__(self):
        return (
            super().__str__() +
            f", Type : Roturier, "
            f"Capacité de production : {self.capacite_production}"
        )