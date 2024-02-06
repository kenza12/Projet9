from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = "Bienvenue sur notre site"
        message = "Bonjour {}, bienvenue sur notre site LITrevu. Votre compte a été créé avec succès.".format(instance.username)
        send_mail(subject, message, 'from@example.com', [instance.email])
