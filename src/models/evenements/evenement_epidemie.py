from .evenement import Evenement
from src.models import Personne, Roturier, Paysan, Noble, Seigneur

class Epidemie(Evenement):
    """
    Un événement qui réduit les ressources d'un personnage.
    """

    def __init__(self, probabilite=0.2, perte_ressources=15):
        super().__init__("Épidémie", probabilite)
        self.perte_ressources = perte_ressources

    def appliquer(self, personnage):
        personnage.diminuer_ressources(self.perte_ressources)
        print(f"{self.nom} : {personnage.nom} perd {self.perte_ressources} ressources.")
