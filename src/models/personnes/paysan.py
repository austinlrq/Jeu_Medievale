from .roturier import Roturier

class Paysan(Roturier):
    """
    Classe représentant un paysan, un type spécifique de roturier.
    """

    def __init__(self, nom: str, age: int, ressources: int, capacite_production: int, bonheur: int):
        super().__init__(nom, age, ressources, 0, capacite_production, bonheur)  # Argent initial à 0

    def __str__(self):
        return (
            super().__str__() +
            f", Type : Paysan"
        )
    
    def to_dict(self):
        # Appel à la méthode to_dict de la classe parente
        return super().to_dict()
