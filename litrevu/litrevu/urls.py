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


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', authentication.views.AuthView.as_view(), name='auth'),
    path('logout/', auth_views.LogoutView.as_view(next_page='auth'), name='logout'),
    path('feed/', activity_feed.views.FeedView.as_view(), name='feed'),
    path('tickets/', ticket.views.TicketListView.as_view(), name='ticket_list'),
    path('reviews/', reviews.views.ReviewListView.as_view(), name='review_list'),
    path('reviews/new_with_ticket/', reviews.views.CreateReviewWithTicketView.as_view(), name='create_review_with_ticket'),
    path('reviews/new_for_ticket/', reviews.views.CreateReviewForTicketView.as_view(), name='create_review_for_ticket'),
    path('reviews/<int:pk>/edit/', reviews.views.UpdateReviewView.as_view(), name='update_review'),
    path('reviews/<int:pk>/delete/', reviews.views.DeleteReviewView.as_view(), name='delete_review'),
    path('tickets/create/', ticket.views.CreateTicketView.as_view(), name='create_ticket'),
    path('tickets/<int:pk>/edit/', ticket.views.UpdateTicketView.as_view(), name='update_ticket'),
    path('tickets/<int:pk>/delete/', ticket.views.DeleteTicketView.as_view(), name='delete_ticket'),
    path('follow/', user_following.views.FollowUserView.as_view(), name='follow_user'),
    path('unfollow/<int:user_id>/', user_following.views.UnfollowUserView.as_view(), name='unfollow'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)