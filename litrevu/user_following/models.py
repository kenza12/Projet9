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

class UserBlocks(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name='blocking',
        on_delete=models.CASCADE
    )
    blocked_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name='blocked_by',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('user', 'blocked_user', )

    def __str__(self):
        return f"{self.user} blocks {self.blocked_user}"
