class MapZoom:
    def __init__(self, canvas, map_manager):
        self.canvas = canvas
        self.map_manager = map_manager  # Référence pour redessiner la carte visible
        self.case_size = map_manager.case_size

        # Activer les bindings pour le zoom
        self.canvas.bind("<MouseWheel>", self.sur_scroll)  # Windows
        self.canvas.bind("<Button-4>", self.sur_scroll_linux)  # Linux/Mac (zoom in)
        self.canvas.bind("<Button-5>", self.sur_scroll_linux)  # Linux/Mac (zoom out)

    def sur_scroll(self, event):
        delta = event.delta
        self.mettre_a_jour_zoom(delta)

    def sur_scroll_linux(self, event):
        if event.num == 4:  # Scroll up
            delta = 120
        elif event.num == 5:  # Scroll down
            delta = -120
        self.mettre_a_jour_zoom(delta)

    def mettre_a_jour_zoom(self, delta):
        facteur_zoom = 5  # Ajustez ce facteur
        nouvelle_taille = self.case_size + (facteur_zoom if delta > 0 else -facteur_zoom)
        nouvelle_taille = max(20, min(nouvelle_taille, 100))  # Limiter entre 20 et 100

        if nouvelle_taille != self.case_size:
            self.case_size = nouvelle_taille
            self.map_manager.case_size = nouvelle_taille  # Mettre à jour la taille dans le map_manager

            # Recalculer le nombre de colonnes et lignes visibles
            self.map_manager.nb_colonnes_visibles = self.canvas.winfo_width() // self.case_size
            self.map_manager.nb_lignes_visibles = self.canvas.winfo_height() // self.case_size

            # Ajuster les compensateurs
            max_compenser_x = len(self.map_manager.grid[0]) - self.map_manager.nb_colonnes_visibles
            max_compenser_y = len(self.map_manager.grid) - self.map_manager.nb_lignes_visibles

            self.map_manager.map_compenser_x = min(self.map_manager.map_compenser_x, max_compenser_x)
            self.map_manager.map_compenser_y = min(self.map_manager.map_compenser_y, max_compenser_y)

            self.map_manager.dessiner_map_visible()
