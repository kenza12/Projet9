from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login, authenticate
from django.views.generic import View
from django.conf import settings
from django.contrib import messages


class AuthView(View):
    def get(self, request):
        login_form = CustomAuthenticationForm()
        signup_form = CustomUserCreationForm()
        return render(request, 'authentication/auth.html', {'login_form': login_form, 'signup_form': signup_form})

    def post(self, request):
        # Initialisation des formulaires
        login_form = CustomAuthenticationForm(data=request.POST if 'login' in request.POST else None)
        signup_form = CustomUserCreationForm(data=request.POST if 'signup' in request.POST else None, files=request.FILES if 'signup' in request.POST else None)

        if 'login' in request.POST:
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    return redirect(settings.LOGIN_REDIRECT_URL)
                else:
                    for error in login_form.errors.values():
                        messages.error(request, error, extra_tags='login')
            else:
                # Traitement des erreurs de formulaire
                for error in login_form.errors.values():
                    messages.error(request, error, extra_tags='login')

        elif 'signup' in request.POST:
            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                for error in signup_form.errors.values():
                    messages.error(request, error, extra_tags='signup')

        return render(request, 'authentication/auth.html', {'login_form': login_form, 'signup_form': signup_form})
