from django.db import models


class ReasonChoices(models.TextChoices):
    SPAM = 'Spam', 'Spam'
    HARASSMENT = 'Harassment', 'Harassment'
    IMPERSONATION = 'Impersonation', 'Impersonation'
    INAPPROPRIATE_CONTENT = 'Inappropriate Content', 'Inappropriate Content'
    OFFENSIVE_LANGUAGE = 'Offensive Language', 'Offensive Language'
    OTHER = 'Other', 'Other'


class StatusChoices(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    RESOLVED = 'Resolved', 'Resolved'
    DISMISSED = 'Dismissed', 'Dismissed'
