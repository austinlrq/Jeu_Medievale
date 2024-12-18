# main.py
import tkinter as tk
# from src.controllers import GameController
# from src.models import Roturier, Paysan
from src.views import MenuPrincipal 

def main():

    # Lancement de l'application
    root = tk.Tk()
    menu_principal = MenuPrincipal(root)
    root.mainloop()

if __name__ == "__main__":
    main()