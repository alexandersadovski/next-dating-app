from django.contrib.auth import get_user_model
from django.db import models


class UserInteraction(models.Model):
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='interactions_made',
    )
    target_user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='interactions_received',
    )
    liked = models.BooleanField()

    class Meta:
        unique_together = ('user', 'target_user')

    @classmethod
    def check_match(cls, user1, user2):
        return cls.objects.filter(
            user=user1,
            target_user=user2,
            liked=True,
        ).exists() and cls.objects.filter(
            user=user2,
            target_user=user1,
            liked=True,
        ).exists()

    def __str__(self):
        status = "Liked" if self.liked else "Not Liked"
        return f'{self.user.email} -> {self.target_user.email}: {status}'  # type: ignore
