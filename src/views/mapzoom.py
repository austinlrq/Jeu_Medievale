class MapZoom:
    def __init__(self, canvas, map_manager):
        self.canvas = canvas
        self.map_manager = map_manager  # Référence pour redessiner la carte visible
        self.case_size = map_manager.case_size

        # Activer les bindings pour le zoom
        self.canvas.bind("<MouseWheel>", self.sur_scroll)  # Windows
        self.canvas.bind("<Button-4>", self.sur_scroll_linux)  # Linux/Mac (zoom in)
        self.canvas.bind("<Button-5>", self.sur_scroll_linux)  # Linux/Mac (zoom out)
        self.canvas.bind("<Configure>", self.on_resize)

    def sur_scroll(self, event):
        delta = event.delta
        self.mettre_a_jour_zoom(delta, event)

    def sur_scroll_linux(self, event):
        if event.num == 4:  # Scroll up
            delta = 120
        elif event.num == 5:  # Scroll down
            delta = -120
        self.mettre_a_jour_zoom(delta, event)


    def mettre_a_jour_zoom(self, delta, event=None):
        facteur_zoom = 5  # Ajustez ce facteur

        # Taille estimée après zoom
        dezoom_max = (self.map_manager.canvas.winfo_width() // self.map_manager.width_map) + 1
        taille_estime = self.case_size + (facteur_zoom if delta > 0 else -facteur_zoom)
        nouvelle_taille = max(dezoom_max, min(taille_estime, 50))  # Limiter entre dezoom_max et 50

        if nouvelle_taille != self.case_size:
            # Calcul de la position relative de la souris
            if event:
                souris_canvas_x = event.x
                souris_canvas_y = event.y
            else:
                # Pour les zooms du resize
                souris_canvas_x = self.canvas.winfo_width() // 2
                souris_canvas_y = self.canvas.winfo_height() // 2

            souris_case_x = souris_canvas_x // self.case_size + self.map_manager.map_compenser_x
            souris_case_y = souris_canvas_y // self.case_size + self.map_manager.map_compenser_y

            # Mettre à jour la taille de la case
            self.case_size = nouvelle_taille
            self.map_manager.case_size = self.case_size

            # Recalculer les dimensions visibles
            self.map_manager.nb_colonnes_visibles = self.canvas.winfo_width() // self.case_size
            self.map_manager.nb_lignes_visibles = self.canvas.winfo_height() // self.case_size

            # Ajuster les compensateurs pour centrer le zoom sur la souris
            self.map_manager.map_compenser_x = max(
                0,
                min(
                    len(self.map_manager.grid[0]) - self.map_manager.nb_colonnes_visibles,
                    souris_case_x - souris_canvas_x // self.case_size
                )
            )
            self.map_manager.map_compenser_y = max(
                0,
                min(
                    len(self.map_manager.grid) - self.map_manager.nb_lignes_visibles,
                    souris_case_y - souris_canvas_y // self.case_size
                )
            )

            # Redessiner la carte
        self.map_manager.dessiner_map_visible()


    def on_resize(self, event):
        self.mettre_a_jour_zoom(0)