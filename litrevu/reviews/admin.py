from django.contrib import admin
from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=[(i, i) for i in range(0, 6)])  # Choix de 0 à 5

    class Meta:
        model = Review
        fields = '__all__'  # Inclure tous les champs

# Définir un ReviewAdmin personnalisé utilisant le formulaire ci-dessus
class ReviewAdmin(admin.ModelAdmin):
    form = ReviewForm
    list_display = ('headline', 'rating', 'user', 'ticket', 'time_created')
    search_fields = ('headline', 'user__username', 'ticket__title')
    list_filter = ('rating', 'time_created')

# Enregistrer le ReviewAdmin personnalisé
admin.site.register(Review, ReviewAdmin)
