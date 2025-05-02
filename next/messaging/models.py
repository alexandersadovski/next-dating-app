from django.contrib.auth import get_user_model
from django.db import models


class Message(models.Model):
    sender = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='sent_messages',
    )
    receiver = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='received_messages',
    )
    content = models.TextField()
    timestamp = models.DateTimeField(
        auto_now_add=True,
    )
    deleted_by_sender = models.BooleanField(
        default=False,
    )
    deleted_by_receiver = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f"Message from {self.sender.email} to {self.receiver.email}"  # type: ignore
