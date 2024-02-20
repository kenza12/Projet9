from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):
    """
    Form for creating or updating a ticket.

    This form allows users to create or update a ticket with fields for title, description, and image.
    """
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        labels = {
            'title': 'Titre',
            'image': 'Image'
        }