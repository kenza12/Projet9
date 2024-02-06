from django.views import View
from django.shortcuts import render
from itertools import chain
from django.db.models import CharField, Value
from ticket.models import Ticket
from reviews.models import Review
from user_following.models import UserFollows
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse


class FeedView(LoginRequiredMixin, View):
    """
    Display a feed of reviews and tickets from the user and followed users.

    This view extends Django's View class and uses LoginRequiredMixin to ensure only authenticated
    users can access the feed. It combines reviews and tickets into a single feed, ordered by creation time.
    """
    template_name = 'activity_feed/feed.html'

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Handle GET requests and render the feed.

        Args:
            request (HttpRequest): The incoming request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: Rendered HTML response with the feed context.
        """
        posts = self.get_queryset(request.user)
        print("Number of posts: ", len(posts))
        for post in posts:
            if hasattr(post, 'rating'):
                post.stars = self.get_stars(post.rating)
            else:
                post.stars = [False] * 5  # Pour les tickets sans note

        return render(request, self.template_name, {'posts': posts})
    
    @staticmethod
    def get_stars(rating: int) -> list:
        """Retourne une liste de booléens pour les étoiles de notation."""
        return [i < rating for i in range(5)]

    def get_queryset(self, user: 'CustomUser') -> list:
        """
        Retrieve and combine reviews and tickets viewable by the user.

        Args:
            user (CustomUser): The user for whom the feed is being generated.

        Returns:
            list: A combined list of reviews and tickets sorted by creation time.
        """
        reviews = self.get_users_viewable_reviews(user)
        tickets = self.get_users_viewable_tickets(user)

        # Combine and sort the two types of posts
        combined_posts = sorted(
            chain(reviews, tickets),
            key=lambda post: post.time_created,
            reverse=True
        )

        # Vérifie si l'utilisateur a déjà répondu à un ticket
        for post in combined_posts:
            if hasattr(post, 'ticket'):
                post.has_user_reviewed = Review.objects.filter(ticket=post.ticket, user=user).exists()
                
        print("Combined posts: ", combined_posts)
        return combined_posts

    def get_users_viewable_reviews(self, user: 'CustomUser'):
        """
        Retrieve reviews from the user, users they follow, and reviews responding to the user's tickets.

        Args:
            user (CustomUser): The user whose reviews and the reviews of followed users are to be retrieved.

        Returns:
            QuerySet: A Django QuerySet of reviews.
        """
        followed_users = UserFollows.objects.filter(user=user).values_list('followed_user', flat=True)
        reviews_from_followed_users = Review.objects.filter(user__in=followed_users)
        user_reviews = Review.objects.filter(user=user)

        # Get reviews for tickets created by the user, regardless of the reviewer being followed or not
        reviews_for_user_tickets = Review.objects.filter(ticket__user=user)

        # Combine all QuerySets
        combined_reviews = reviews_from_followed_users | user_reviews | reviews_for_user_tickets

        return combined_reviews.annotate(content_type=Value('REVIEW', CharField()))

    def get_users_viewable_tickets(self, user: 'CustomUser'):
        """
        Retrieve tickets from the user and users they follow.

        Args:
            user (CustomUser): The user whose tickets and the tickets of followed users are to be retrieved.

        Returns:
            QuerySet: A Django QuerySet of tickets.
        """
        followed_users = UserFollows.objects.filter(user=user).values_list('followed_user', flat=True)
        tickets = Ticket.objects.filter(user__in=followed_users) | Ticket.objects.filter(user=user)
        return tickets.annotate(content_type=Value('TICKET', CharField()))
