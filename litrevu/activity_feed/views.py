from django.views import View
from django.shortcuts import render
from itertools import chain
from django.db.models import CharField, Value
from ticket.models import Ticket
from reviews.models import Review
from user_following.models import UserFollows, UserBlocks
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse


class FeedView(LoginRequiredMixin, View):
    """Display a feed of reviews and tickets from the user and followed users.

    This view extends Django's View class and uses LoginRequiredMixin to ensure only authenticated users can access the
    feed. It combines reviews and tickets into a single feed, ordered by creation time.
    """

    template_name = "activity_feed/feed.html"

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Handle GET requests and render the feed.

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
            if hasattr(post, "rating"):
                post.stars = self.get_stars(post.rating)
            else:
                post.stars = [False] * 5  # Pour les tickets sans note

        return render(request, self.template_name, {"posts": posts})

    @staticmethod
    def get_stars(rating: int) -> list:
        """Retourne une liste de booléens pour les étoiles de notation."""
        return [i < rating for i in range(5)]

    def get_queryset(self, user: "CustomUser") -> list:
        """Retrieve and combine reviews and tickets viewable by the user.

        Args:
            user (CustomUser): The user for whom the feed is being generated.

        Returns:
            list: A combined list of reviews and tickets sorted by creation time.
        """
        # Obtenez les IDs des utilisateurs bloqués et des bloqueurs
        blocked_users_ids = UserBlocks.objects.filter(user=user).values_list("blocked_user", flat=True)
        blocking_users_ids = UserBlocks.objects.filter(blocked_user=user).values_list("user", flat=True)

        # Obtenez les IDs des utilisateurs suivis, en excluant les utilisateurs bloqués/bloqueurs
        followed_users = (
            UserFollows.objects.filter(user=user)
            .exclude(followed_user__in=blocked_users_ids)
            .exclude(followed_user__in=blocking_users_ids)
            .values_list("followed_user", flat=True)
        )

        # Filtrez les reviews et tickets pour exclure ceux des utilisateurs bloqués et bloqueurs
        reviews = self.get_users_viewable_reviews(user, followed_users, blocked_users_ids, blocking_users_ids)
        tickets = self.get_users_viewable_tickets(user, followed_users, blocked_users_ids, blocking_users_ids)

        # Combine et trie les deux types de posts
        combined_posts = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)

        # Vérifie si l'utilisateur a déjà répondu à un ticket
        for post in combined_posts:
            if hasattr(post, "ticket"):
                post.has_user_reviewed = Review.objects.filter(ticket=post.ticket, user=user).exists()

        print("Combined posts: ", combined_posts)
        return combined_posts

    def get_users_viewable_reviews(self, user, followed_users, blocked_users_ids, blocking_users_ids):
        """Récupère les critiques ('reviews') visibles par l'utilisateur.

        Cette méthode permet de filtrer et de retourner les critiques qui sont visibles par l'utilisateur donné.
        Elle inclut les critiques des utilisateurs suivis par l'utilisateur (sauf ceux bloqués), ainsi que ses propres critiques.
        Les critiques en réponse aux tickets de l'utilisateur sont également incluses, même si l'auteur de la critique n'est pas suivi par l'utilisateur.

        Args:
            user (CustomUser): L'utilisateur pour lequel la liste des critiques est récupérée.
            followed_users (QuerySet): Les utilisateurs que l'utilisateur suit.
            blocked_users_ids (list): Les identifiants des utilisateurs bloqués par l'utilisateur.
            blocking_users_ids (list): Les identifiants des utilisateurs qui ont bloqué l'utilisateur.

        Returns:
            QuerySet: Un QuerySet des critiques filtrées, annoté avec un champ 'content_type' pour identifier le type de contenu.
        """

        # Combine les IDs des utilisateurs bloqués et bloqueurs
        excluded_users_ids = set(blocked_users_ids).union(set(blocking_users_ids))

        # Filtre les reviews des utilisateurs suivis et de l'utilisateur, en excluant les utilisateurs bloqués/bloqueurs
        reviews = Review.objects.filter(user__in=followed_users).exclude(user__in=excluded_users_ids)

        # Inclure les propres reviews de l'utilisateur, en excluant celles liées aux tickets des utilisateurs bloqués/bloqueurs
        user_reviews = Review.objects.filter(user=user).exclude(ticket__user__in=excluded_users_ids)

        # Inclure les reviews en réponse aux tickets de l'utilisateur (même si l'utilisateur ne suit pas l'auteur de la review)
        reviews_to_user_tickets = Review.objects.filter(ticket__user=user).exclude(user__in=excluded_users_ids)

        # Combine user's own reviews, reviews from followed users, and reviews to user's tickets
        combined_reviews = reviews | user_reviews | reviews_to_user_tickets

        return combined_reviews.annotate(content_type=Value("REVIEW", CharField()))

    def get_users_viewable_tickets(self, user, followed_users, blocked_users_ids, blocking_users_ids):
        """Récupère les tickets visibles par l'utilisateur.

        Cette méthode filtre et retourne les tickets qui sont visibles par l'utilisateur donné.
        Elle inclut les tickets des utilisateurs suivis par l'utilisateur, ainsi que ses propres tickets,
        en excluant les tickets des utilisateurs bloqués ou qui ont bloqué l'utilisateur.

        Args:
            user (CustomUser): L'utilisateur pour lequel la liste des tickets est récupérée.
            followed_users (QuerySet): Les utilisateurs que l'utilisateur suit.
            blocked_users_ids (list): Les identifiants des utilisateurs bloqués par l'utilisateur.
            blocking_users_ids (list): Les identifiants des utilisateurs qui ont bloqué l'utilisateur.

        Returns:
            QuerySet: Un QuerySet des tickets filtrés, annoté avec un champ 'content_type' pour identifier le type de contenu.
        """

        # Combine les IDs des utilisateurs bloqués et bloqueurs
        excluded_users_ids = set(blocked_users_ids).union(set(blocking_users_ids))

        # Filter tickets from followed users and the user, excluding blocked/blocking users
        tickets = Ticket.objects.filter(user__in=set(followed_users).union({user.id})).exclude(
            user__in=excluded_users_ids
        )

        return tickets.annotate(content_type=Value("TICKET", CharField()))
