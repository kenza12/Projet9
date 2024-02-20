from django.apps import AppConfig


class ActivityFeedConfig(AppConfig):
    """
    Configuration de l'application pour le module 'activity_feed'.

    Attributes:
        default_auto_field (str): Spécifie le type de champ à utiliser pour les champs d'auto-incrémentation.
        name (str): Le nom de l'application. Utilisé pour faire référence à l'application dans Django, comme dans les 'INSTALLED_APPS'.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "activity_feed"
