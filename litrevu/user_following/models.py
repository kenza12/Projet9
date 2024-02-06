from django.db import models
from django.conf import settings


class UserFollows(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, 
        related_name='following',
        on_delete=models.CASCADE
    )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, 
        related_name='followers',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('user', 'followed_user', )

    def __str__(self):
        return f"{self.user} follows {self.followed_user}"
