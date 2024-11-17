from .evenement import Evenement
from src.models import Personne, Roturier, Paysan, Noble, Seigneur

class RecolteAbondante(Evenement):
    """
    Un événement qui augmente les ressources d'un personnage.
    """

    def __init__(self, probabilite=0.3, gain_ressources=20):
        super().__init__("Récolte Abondante", probabilite)
        self.gain_ressources = gain_ressources

    def appliquer(self, personnage):
        if isinstance(personnage, Roturier) or isinstance(personnage, Paysan):
            personnage.augmenter_ressources(self.gain_ressources)
            print(f"{self.nom} : {personnage.nom} gagne {self.gain_ressources} ressources.")
