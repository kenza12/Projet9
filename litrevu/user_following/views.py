from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserFollowForm
from .models import UserFollows
from authentication.models import CustomUser

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
        followed_users = UserFollows.objects.filter(user=request.user)
        followers = UserFollows.objects.filter(followed_user=request.user)
        return render(request, 'user_following/follow.html', {
            'form': form,
            'followed_users': followed_users,
            'followers': followers
        })

    def post(self, request: 'HttpRequest') -> 'HttpResponseRedirect':
        """
        Handles the POST request.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            HttpResponseRedirect: A redirect to a new URL.
        """
        form = UserFollowForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            followed_user = CustomUser.objects.get(username=username)
            if followed_user != request.user:
                UserFollows.objects.get_or_create(user=request.user, followed_user=followed_user)
            return redirect('follow_user')
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
