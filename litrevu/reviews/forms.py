from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['ticket', 'rating', 'headline', 'body']
        labels = {
            'rating': 'Note',
            'headline': 'Titre',
            'body': 'Commentaire'
        }

class ReviewFormWithoutTicket(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'headline', 'body']
        labels = {
            'rating': 'Note',
            'headline': 'Titre',
            'body': 'Commentaire'
        }