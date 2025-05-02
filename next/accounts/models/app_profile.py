from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from next.accounts.choices import GenderChoices
from next.accounts.validators import FileSizeValidator


class Profile(models.Model):
    user = models.OneToOneField(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='profile',
        primary_key=True,
    )
    first_name = models.CharField(
        max_length=25,
    )
    last_name = models.CharField(
        max_length=25,
    )
    age = models.IntegerField(
        validators=[
            MinValueValidator(18),
        ]
    )
    gender = models.CharField(
        max_length=25,
        choices=GenderChoices.choices,
    )
    location = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    bio = models.TextField(
        null=True,
        blank=True,
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures',
        validators=[
            FileSizeValidator(5),
        ],
        null=True,
        blank=True,
    )

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.get_full_name()
