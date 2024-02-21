# user_following/forms.py
from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class UserFollowForm(forms.Form):
    """
    Form for following a user.

    Attributes:
        username (str): CharField for entering the username of the user to follow.
    """

    username = forms.CharField(label="Nom d’utilisateur", max_length=150)

    def clean_username(self):
        """
        Validates the entered username.

        Returns:
            str: The validated username.

        Raises:
            forms.ValidationError: If the entered username does not exist in the database.
        """
        username = self.cleaned_data["username"]
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Cet utilisateur n'existe pas.")
        return username
