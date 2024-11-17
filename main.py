from src.controllers import *
from src.models import *
from src.views import *
import tkinter as tk

#gamecontroller = GameController()


# Ajout d'habitants
"""for i in range(5):
    village_joueur.ajouter_habitant(Roturier(f"Roturier {i+1}", age=20 + i))
for i in range(3):
    village_joueur.ajouter_habitant(Paysan(f"Paysan {i+1}", age=25 + i))"""


# Lancement de l'application
root = tk.Tk()
menu_principal = MenuPrincipal(root)
root.mainloop()