# main.py
import tkinter as tk

def main():
    from src.controllers import GameController
    from src.models import Roturier, Paysan
    from src.views import MenuPrincipal

    # Ajout d'habitants
    """for i in range(5):
        village_joueur.ajouter_habitant(Roturier(f"Roturier {i+1}", age=20 + i))
    for i in range(3):
        village_joueur.ajouter_habitant(Paysan(f"Paysan {i+1}", age=25 + i))"""

    # Lancement de l'application
    root = tk.Tk()
    menu_principal = MenuPrincipal(root)
    root.mainloop()

if __name__ == "__main__":
    main()