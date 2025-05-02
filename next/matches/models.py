from django.contrib.auth import get_user_model
from django.db import models


class Match(models.Model):
    user1 = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='matches_as_user1',
    )
    user2 = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='matches_as_user2',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = ('user1', 'user2')

    @classmethod
    def create_match(cls, user1, user2):
        if not cls.objects.filter(
                user1=user1,
                user2=user2
        ).exists() and not cls.objects.filter(
            user1=user2,
            user2=user1
        ).exists():
            cls.objects.create(
                user1=user1,
                user2=user2,
            )

    def __str__(self):
        return f"Match between {self.user1.email} and {self.user2.email}"  # type: ignore
