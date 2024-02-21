from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserFollowForm
from .models import UserFollows, UserBlocks
from authentication.models import CustomUser
from django.contrib import messages


class FollowUserView(LoginRequiredMixin, View):
    """
    This class handles operations for following a user.
    """

    def get(self, request: "HttpRequest") -> "HttpResponse":
        """
        Renders the follow user page, allowing users to follow, unfollow, block, or unblock other users.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            HttpResponse: The rendered response.
        """

        form = UserFollowForm()

        blocked_users_ids = UserBlocks.objects.filter(user=request.user).values_list("blocked_user", flat=True)

        blocked_users = CustomUser.objects.filter(id__in=blocked_users_ids)

        followed_users = UserFollows.objects.filter(user=request.user).exclude(followed_user__in=blocked_users)

        followers = UserFollows.objects.filter(followed_user=request.user).exclude(user__in=blocked_users)

        # Obtenir les ID des utilisateurs que l'utilisateur actuel a bloqués
        user_blocked_ids = set(UserBlocks.objects.filter(user=request.user).values_list("blocked_user_id", flat=True))

        return render(
            request,
            "user_following/follow.html",
            {
                "form": form,
                "followed_users": followed_users,
                "followers": followers,
                "blocked_users": blocked_users,
                "user_blocked_ids": user_blocked_ids,
            },
        )

    def post(self, request: "HttpRequest") -> "HttpResponseRedirect":
        """
        Handles the POST requests for following a user.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            HttpResponseRedirect: Redirects to the follow user page.
        """

        form = UserFollowForm(request.POST)

        if form.is_valid():
            # Récupération du nom d'utilisateur nettoyé à partir des données de formulaire
            username = form.cleaned_data["username"]

            try:
                followed_user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                messages.error(request, "Cet utilisateur n'existe pas.")
                return self.get(request)

            # Vérification si l'utilisateur courant est bloqué par l'utilisateur qu'il tente de suivre
            if UserBlocks.objects.filter(user=followed_user, blocked_user=request.user).exists():
                messages.error(request, "Vous ne pouvez pas suivre cet utilisateur.")
                return redirect("follow_user")

            # Si l'utilisateur courant n'est pas bloqué, créer ou récupérer l'objet UserFollows
            if followed_user != request.user:
                UserFollows.objects.get_or_create(user=request.user, followed_user=followed_user)

            return redirect("follow_user")
        else:
            # Si le formulaire n'est pas valide, afficher les erreurs du formulaire
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return self.get(request)


class UnfollowUserView(LoginRequiredMixin, View):
    """
    Handles operations for unfollowing a user.
    """

    def get(self, request: "HttpRequest", user_id: int) -> "HttpResponseRedirect":
        """
        Handles the GET request to unfollow a user.

        Args:
            request (HttpRequest): The incoming HTTP request.
            user_id (int): The ID of the user to unfollow.

        Returns:
            HttpResponseRedirect: A redirect to a new URL.
        """
        return self.post(request, user_id)

    def post(self, request: "HttpRequest", user_id: int) -> "HttpResponseRedirect":
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
        return redirect("follow_user")


class BlockUserView(LoginRequiredMixin, View):
    def post(self, request: "HttpRequest", user_id: int) -> "HttpResponseRedirect":
        blocked_user = CustomUser.objects.get(pk=user_id)
        UserBlocks.objects.get_or_create(user=request.user, blocked_user=blocked_user)
        return redirect("follow_user")


class UnblockUserView(LoginRequiredMixin, View):
    """
    Handles unblocking a user.
    """

    def post(self, request: "HttpRequest", user_id: int) -> "HttpResponseRedirect":
        """
        Handles the POST request to unblock a user.

        Args:
            request (HttpRequest): The incoming HTTP request.
            user_id (int): The ID of the user to unblock.

        Returns:
            HttpResponseRedirect: Redirects to the follow user page.
        """

        # Vérifier si l'utilisateur actuel a bloqué cet utilisateur
        block = UserBlocks.objects.filter(user=request.user, blocked_user_id=user_id)

        if block.exists():
            block.delete()
        return redirect("follow_user")
