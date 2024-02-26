from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Adds an email field and customizes widget placeholders."""

    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"placeholder": "Adresse e-mail"}))

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "profile_photo",
        )

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"placeholder": "* Nom d'utilisateur"})
        self.fields["password1"].widget.attrs.update({"placeholder": "* Mot de passe"})
        self.fields["password2"].widget.attrs.update({"placeholder": "* Confirmation du mot de passe"})
        self.fields["first_name"].widget.attrs.update({"placeholder": "* Prénom"})
        self.fields["last_name"].widget.attrs.update({"placeholder": "* Nom"})
        self.fields["email"].widget.attrs.update({"placeholder": "* Adresse e-mail"})


class CustomAuthenticationForm(AuthenticationForm):
    """Customizes widget placeholders for 'username' and 'password' fields."""

    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"placeholder": "* Nom d'utilisateur"})
        self.fields["password"].widget.attrs.update({"placeholder": "* Mot de passe"})
