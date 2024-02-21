def get_stars(rating):
    """Retourne une liste de booléens pour les étoiles de notation."""
    return [i < rating for i in range(5)]
