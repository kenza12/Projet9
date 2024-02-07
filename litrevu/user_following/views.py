from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserFollowForm
from .models import UserFollows, UserBlocks
from authentication.models import CustomUser
from django.contrib import messages

class FollowUserView(LoginRequiredMixin, View):
    """
    This class, inheriting from LoginRequiredMixin and View, handles operations for following a user.
    It supports GET and POST requests:
    - GET: Renders the follow user page.
    - POST: Processes the form to follow a user.
    """

    def get(self, request: 'HttpRequest') -> 'HttpResponse':
        """
        Handles the GET request.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            HttpResponse: The rendered response.
        """
        form = UserFollowForm()
        blocked_users_ids = UserBlocks.objects.filter(user=request.user).values_list('blocked_user', flat=True)
        blocked_users = CustomUser.objects.filter(id__in=blocked_users_ids)

        followed_users = UserFollows.objects.filter(user=request.user).exclude(followed_user__in=blocked_users)
        followers = UserFollows.objects.filter(followed_user=request.user).exclude(user__in=blocked_users)
         # Obtenez les ID des utilisateurs que l'utilisateur actuel a bloqués
        user_blocked_ids = set(UserBlocks.objects.filter(user=request.user).values_list('blocked_user_id', flat=True))

        return render(request, 'user_following/follow.html', {
            'form': form,
            'followed_users': followed_users,
            'followers': followers,
            'blocked_users': blocked_users,
            'user_blocked_ids': user_blocked_ids
        })

    def post(self, request: 'HttpRequest') -> 'HttpResponseRedirect':
        """
        Gère les requêtes POST pour suivre un utilisateur.

        Args:
            request (HttpRequest): La requête HTTP entrante.

        Returns:
            HttpResponseRedirect: Redirige vers une nouvelle URL.
        """
        # Création d'une instance du formulaire avec les données POST
        form = UserFollowForm(request.POST)

        # Vérification si le formulaire est valide
        if form.is_valid():
            # Récupération du nom d'utilisateur nettoyé à partir des données de formulaire
            username = form.cleaned_data['username']

            # Tentative de récupération de l'utilisateur à suivre
            try:
                followed_user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                # Si l'utilisateur n'existe pas, afficher un message d'erreur
                messages.error(request, "Cet utilisateur n'existe pas.")
                return self.get(request)

            # Vérification si l'utilisateur courant est bloqué par l'utilisateur qu'il tente de suivre
            if UserBlocks.objects.filter(user=followed_user, blocked_user=request.user).exists():
                # Si bloqué, ne pas permettre de suivre et afficher un message d'erreur
                messages.error(request, "Vous ne pouvez pas suivre cet utilisateur.")
                return redirect('follow_user')

            # Si l'utilisateur courant n'est pas bloqué, créer ou récupérer l'objet UserFollows
            if followed_user != request.user:
                UserFollows.objects.get_or_create(user=request.user, followed_user=followed_user)

            return redirect('follow_user')
        else:
            # Si le formulaire n'est pas valide, afficher les erreurs du formulaire
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

            # Renvoyer l'utilisateur à la page avec le formulaire et les messages d'erreur
            return self.get(request)


class UnfollowUserView(LoginRequiredMixin, View):
    """
    This class, inheriting from LoginRequiredMixin and View, handles operations for unfollowing a user.
    It supports both GET and POST requests, but both perform the same operation of unfollowing a user.
    """

    def get(self, request: 'HttpRequest', user_id: int) -> 'HttpResponseRedirect':
        """
        Handles the GET request to unfollow a user.

        Args:
            request (HttpRequest): The incoming HTTP request.
            user_id (int): The ID of the user to unfollow.

        Returns:
            HttpResponseRedirect: A redirect to a new URL.
        """
        return self.post(request, user_id)

    def post(self, request: 'HttpRequest', user_id: int) -> 'HttpResponseRedirect':
        """
        Handles the POST request to unfollow a user.

        Args:
            request (HttpRequest): The incoming HTTP request.
            user_id (int): The ID of the user to unfollow.

        Returns:
            HttpResponseRedirect: A redirect to a new URL.
        """
        followed_user = CustomUser.objects.get(pk=user_id)
        UserFollows.objects.filter(user=request.user, followed_user=followed_user).delete()
        return redirect('follow_user')

class BlockUserView(LoginRequiredMixin, View):
    def post(self, request: 'HttpRequest', user_id: int) -> 'HttpResponseRedirect':
        blocked_user = CustomUser.objects.get(pk=user_id)
        UserBlocks.objects.get_or_create(user=request.user, blocked_user=blocked_user)
        return redirect('follow_user')

class UnblockUserView(LoginRequiredMixin, View):
    def post(self, request: 'HttpRequest', user_id: int) -> 'HttpResponseRedirect':
        # Vérifier si l'utilisateur actuel a bloqué cet utilisateur
        block = UserBlocks.objects.filter(user=request.user, blocked_user_id=user_id)
        if block.exists():
            block.delete()
        return redirect('follow_user')