from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
import authentication.views
import activity_feed.views
import ticket.views
import reviews.views
import user_following.views
from django.conf import settings
from django.conf.urls.static import static


# Définition des URLs de l'application

urlpatterns = [
    path("admin/", admin.site.urls),  # URL pour l'interface d'administration Django
    path("", authentication.views.AuthView.as_view(), name="auth"),  # URL pour l'authentification des utilisateurs
    path(
        "logout/", auth_views.LogoutView.as_view(next_page="auth"), name="logout"
    ),  # URL pour la déconnexion des utilisateurs
    path("feed/", activity_feed.views.FeedView.as_view(), name="feed"),  # URL pour le flux d'activité
    path(
        "tickets/", ticket.views.TicketListView.as_view(), name="ticket_list"
    ),  # URL pour la page posts (tickets + reviews) de l'user connecté
    path(
        "reviews/new_with_ticket/",
        reviews.views.CreateReviewWithTicketView.as_view(),
        name="create_review_with_ticket",
    ),  # URL pour créer une critique avec un ticket
    path(
        "reviews/new_for_ticket/", reviews.views.CreateReviewForTicketView.as_view(), name="create_review_for_ticket"
    ),  # URL pour créer une critique en réponse à un ticket
    path(
        "reviews/<int:pk>/edit/", reviews.views.UpdateReviewView.as_view(), name="update_review"
    ),  # URL pour mettre à jour une critique
    path(
        "reviews/<int:pk>/delete/", reviews.views.DeleteReviewView.as_view(), name="delete_review"
    ),  # URL pour supprimer une critique
    path("tickets/create/", ticket.views.CreateTicketView.as_view(), name="create_ticket"),  # URL pour créer un ticket
    path(
        "tickets/<int:pk>/edit/", ticket.views.UpdateTicketView.as_view(), name="update_ticket"
    ),  # URL pour mettre à jour un ticket
    path(
        "tickets/<int:pk>/delete/", ticket.views.DeleteTicketView.as_view(), name="delete_ticket"
    ),  # URL pour supprimer un ticket
    path(
        "follow/", user_following.views.FollowUserView.as_view(), name="follow_user"
    ),  # URL pour suivre un utilisateur
    path(
        "unfollow/<int:user_id>/", user_following.views.UnfollowUserView.as_view(), name="unfollow"
    ),  # URL pour ne plus suivre un utilisateur
    path(
        "block-user/<int:user_id>/", user_following.views.BlockUserView.as_view(), name="block_user"
    ),  # URL pour bloquer un utilisateur
    path(
        "unblock-user/<int:user_id>/", user_following.views.UnblockUserView.as_view(), name="unblock_user"
    ),  # URL pour débloquer un utilisateur
]

# Si le mode DEBUG est activé, les URLs des fichiers média sont également ajoutées
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
