from django.contrib import admin
from .models import UserFollows


class UserFollowsAdmin(admin.ModelAdmin):
    """
    Customizes the UserFollows admin interface to display and search user follow relationships.

    Attributes:
        list_display (tuple): The usernames of the user and the followed user.
        search_fields (tuple): Specifies the fields to enable search functionality in the admin interface. Allows searching by the usernames of both the user and the followed user.
    """

    list_display = ("user", "followed_user")
    search_fields = ("user__username", "followed_user__username")


admin.site.register(UserFollows, UserFollowsAdmin)
