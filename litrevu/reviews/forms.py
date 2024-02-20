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
        widgets = {
            'rating': forms.Select(choices=[(n, n) for n in range(6)]),
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
        widgets = {
            'rating': forms.Select(choices=[(n, n) for n in range(6)]),
        }