import tkinter as tk
from tkinter import ttk

def ajouter_texte():
    texte = "Nouveau texte ajouté.\n"
    zone_texte.insert(tk.END, texte)  # Ajoute à la fin de la zone de texte
    zone_texte.see(tk.END)  # Scrolle automatiquement vers la fin

root = tk.Tk()
root.title("Ajouter du texte à la fin")

# Zone de texte
zone_texte = tk.Text(root, width=50, height=10, wrap="word")
zone_texte.pack(pady=10)

# Bouton pour ajouter du texte
btn_ajouter = ttk.Button(root, text="Ajouter Texte", command=ajouter_texte)
btn_ajouter.pack(pady=5)

root.mainloop()
