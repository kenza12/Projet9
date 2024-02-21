from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour le modèle CustomUser.

    Cette classe définit la présentation et les fonctionnalités disponibles
    dans l'interface d'administration de Django pour le modèle CustomUser.
    Elle permet de personnaliser l'affichage des utilisateurs dans la liste,
    ainsi que les champs utilisables pour la recherche.

    Attributs:
        list_display (tuple): Définit les champs à afficher dans la liste des utilisateurs.
        search_fields (tuple): Définit les champs sur lesquels les recherches peuvent être effectuées.
    """

    list_display = ("username", "first_name", "last_name", "email", "is_staff")
    search_fields = ("username", "first_name", "last_name", "email")


# Enregistrement du modèle CustomUser avec la configuration CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
