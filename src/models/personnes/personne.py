import random

class Personne:
    """
    Classe de base pour représenter une personne dans la société médiévale.
    """

    def __init__(self, nom: str, age: int, ressources: int, argent: int, bonheur: int):
        self.nom = nom
        self.age = age
        self.esperance_de_vie = random.randint(60, 80)
        self.ressources = ressources
        self.argent = argent
        self.bonheur = bonheur

    def __str__(self):
        return (
            f"Nom : {self.nom}, "
            f"Âge : {self.age}, "
            f"Esperence de vie : {self.esperance_de_vie}, "
            f"Ressources : {self.ressources}, "
            f"Argent : {self.argent}, "
            f"Bonheur : {self.bonheur}"
        )
    
    def augmenter_ressources(self, montant: int):
        """Augmente les ressources de la personne de la valeur spécifiée."""
        self.ressources += montant

    def diminuer_ressources(self, montant: int):
        """Diminue les ressources de la personne de la valeur spécifiée, sans aller en dessous de zéro."""
        self.ressources = max(0, self.ressources - montant)

    def augmenter_argent(self, montant: int):
        """Augmente l'argent de la personne de la valeur spécifiée."""
        self.argent += montant

    def diminuer_argent(self, montant: int):
        """Diminue l'argent de la personne de la valeur spécifiée, sans aller en dessous de zéro."""
        self.argent = max(0, self.argent - montant)

    def augmenter_bonheur(self, nombre: int):
        """Augmente le bonheure de la personne spécifiée"""
        self.bonheur += nombre

    def diminuer_bonheur(self, nombre: int):
        """Diminue le bonheure de la personne spécifiée"""
        self.bonheur += max(0, self.argent - nombre)

    def vieillir(self):
        """Augmente l'âge du personnage et vérifie s'il meurt aléatoirement."""
        self.age += 1
        return self.mort_aleatoire()

    def mort_aleatoire(self):
        """Détermine si le personnage meurt en fonction de son âge."""
        chance_de_mort = min((self.age - 50) * 0.05, 0.5)  # Exemple : 5% de plus par an après 50 ans, jusqu'à un max de 50%
        return random.random() < chance_de_mort  # Retourne True si le personnage meurt
    
    def to_dict(self):
        """Convertit l'objet Personne en dictionnaire."""
        return {
            "nom": self.nom,
            "age": self.age,
            "esperance_de_vie": self.esperance_de_vie,
            "ressources": self.ressources,
            "argent": self.argent,
            "bonheur": self.bonheur
        }