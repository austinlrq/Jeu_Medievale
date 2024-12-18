class Soldat:
    def __init__(self, nom, force, type_soldat="Infanterie"):
        self.nom = nom
        self.force = force
        self.type_soldat = type_soldat  # Ex : Infanterie, Archer, Cavalier
    def to_dict(self):
        return {
            "nom": self.nom,
            "force": self.force,
            "type_soldat": self.type_soldat
        }