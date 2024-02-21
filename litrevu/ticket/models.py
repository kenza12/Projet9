from django.db import models
from django.conf import settings


class Ticket(models.Model):
    """
    Model representing a ticket posted by a user.

    Attributes:
        title (CharField): The title of the ticket.
        description (TextField): The description of the ticket.
        user (ForeignKey): The user who posted the ticket.
        image (ImageField): The image attached to the ticket (optional).
        time_created (DateTimeField): The date and time when the ticket was created.
    """

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="ticket_images/", null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
