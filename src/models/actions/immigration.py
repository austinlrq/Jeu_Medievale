from ..personnes import *


class Immigration:
    def __init__(self, noble):
        """
        Initialise l'action d'immigration pour un noble donné.
        :param noble: L'objet Noble pour lequel l'immigration s'applique.
        """
        self.noble = noble
        self.cout_paysan = 5
        self.cout_roturier = 10

    def immigrer(self, type_personne):
        """
        Permet l'immigration d'un paysan ou d'un roturier dans le village du noble.
        :param type_personne: "paysan" pour ajouter un paysan, "roturier" pour ajouter un roturier.
        :return: True si l'immigration a réussi, False sinon.
        """
        if type_personne == "paysan":
            cout = self.cout_paysan
            if self.noble.argent >= cout:
                paysan = Paysan(f"Paysan {len(self.noble.village_noble.habitants) + 1}", 20, 10, 0, 5)
                self.noble.village_noble.ajouter_habitant(paysan)
                self.noble.argent -= cout
                print(f"Un paysan a immigré dans le village de {self.noble.nom}. Argent restant : {self.noble.argent}")
                return True
            else:
                print("Pas assez d'argent pour faire immigrer un paysan.")
                return False

        elif type_personne == "roturier":
            cout = self.cout_roturier
            if self.noble.argent >= cout:
                roturier = Roturier(f"Roturier {len(self.noble.village_noble.habitants) + 1}", 20, 15, 0, 5, 5)
                self.noble.village_noble.ajouter_habitant(roturier)
                self.noble.argent -= cout
                print(f"Un roturier a immigré dans le village de {self.noble.nom}. Argent restant : {self.noble.argent}")
                return True
            else:
                print("Pas assez d'argent pour faire immigrer un roturier.")
                return False

        else:
            print("Type de personne invalide pour l'immigration.")
            return False
