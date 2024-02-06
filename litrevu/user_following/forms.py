# user_following/forms.py
from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()

class UserFollowForm(forms.Form):
    username = forms.CharField(label='Nom d’utilisateur', max_length=150)

    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Cet utilisateur n'existe pas.")
        return username
