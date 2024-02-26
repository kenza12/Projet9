from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """Configuration de l'application 'authentication'.

    Cette classe étend AppConfig pour configurer des aspects spécifiques de
    l'application 'authentication'.

    Attributs:
        name (str): Le nom de l'application, utilisé dans les paramètres
                    Django pour l'identifier.
    """

    name = "authentication"
