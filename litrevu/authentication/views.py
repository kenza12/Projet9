from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login, authenticate
from django.views.generic import View
from django.conf import settings
from django.contrib import messages


class AuthView(View):
    """
    Vue pour l'authentification des utilisateurs.

    Cette classe gère à la fois l'affichage du formulaire de connexion et le traitement
    de la soumission des formulaires de connexion et d'inscription.
    """

    def get(self, request):
        """
        Afficher la page d'authentification.

        Args:
            request: L'objet HttpRequest pour la requête entrante.

        Returns:
            HttpResponse: La réponse HTTP contenant la page d'authentification.
        """

        # Initialisation des formulaires de connexion et d'inscription
        login_form = CustomAuthenticationForm()
        signup_form = CustomUserCreationForm()

        return render(request, 'authentication/auth.html', {'login_form': login_form, 'signup_form': signup_form})

    def post(self, request):
        """
        Gérer la soumission des formulaires de connexion et d'inscription.

        Args:
            request: L'objet HttpRequest pour la requête entrante.

        Returns:
            HttpResponse: La réponse HTTP après le traitement de la soumission du formulaire.
        """

        # Initialisation des formulaires de connexion et d'inscription avec les données de la requête
        login_form = CustomAuthenticationForm(data=request.POST if 'login' in request.POST else None)
        signup_form = CustomUserCreationForm(data=request.POST if 'signup' in request.POST else None, files=request.FILES if 'signup' in request.POST else None)

        if 'login' in request.POST: # Si le formulaire de connexion est soumis
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user: # Si l'authentification réussit
                    login(request, user) # Connexion de l'utilisateur
                    return redirect(settings.LOGIN_REDIRECT_URL)
                else:
                    for error in login_form.errors.values():
                        messages.error(request, error, extra_tags='login')
            else:
                # Traitement des erreurs de formulaire
                for error in login_form.errors.values():
                    messages.error(request, error, extra_tags='login')

        elif 'signup' in request.POST: # Si le formulaire d'inscription est soumis
            if signup_form.is_valid():
                user = signup_form.save() # Enregistrement de l'utilisateur
                login(request, user) # Connexion de l'utilisateur
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                for error in signup_form.errors.values():
                    messages.error(request, error, extra_tags='signup')

        return render(request, 'authentication/auth.html', {'login_form': login_form, 'signup_form': signup_form})
