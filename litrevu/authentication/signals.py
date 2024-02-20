from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    """
    Envoyer un e-mail de bienvenue à un nouvel utilisateur.

    Args:
        sender: La classe du modèle qui envoie le signal (CustomUser).
        instance: L'instance de CustomUser qui a été enregistrée.
        created (bool): Indique si l'instance a été créée ou mise à jour.
        **kwargs: Arguments supplémentaires passés au signal.

    Returns:
        None
    """
    if created:
        subject = "Bienvenue sur notre site"
        message = "Bonjour {}, bienvenue sur notre site LITrevu. Votre compte a été créé avec succès.".format(instance.username)
        send_mail(subject, message, 'from@example.com', [instance.email])
