from src.models import Personne, Roturier, Paysan, Noble, Seigneur
from src.models import Evenement

class EclataxGuerre(Evenement):
    """
    Un événement qui affecte les nobles et seigneurs, diminuant leurs ressources et argent.
    """
    def __init__(self, probabilite=0.1, perte_ressources=30, perte_argent=20):
        super().__init__("Guerre", probabilite)
        self.perte_ressources = perte_ressources
        self.perte_argent = perte_argent

    def appliquer(self, personnage):
        if isinstance(personnage, Noble) or isinstance(personnage, Seigneur):
            personnage.diminuer_ressources(self.perte_ressources)
            personnage.diminuer_argent(self.perte_argent)
            print(f"{self.nom} : {personnage.nom} perd {self.perte_ressources} ressources et {self.perte_argent} pièces d'argent.")
