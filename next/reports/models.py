from django.contrib.auth import get_user_model
from django.db import models
from next.reports.choices import ReasonChoices, StatusChoices


class Report(models.Model):
    reported_by = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='reports_made',
    )
    reported_user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='reports_received',
    )
    reason = models.CharField(
        max_length=25,
        choices=ReasonChoices.choices,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    status = models.CharField(
        max_length=25,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
    )

    def __str__(self):
        return (
            f"Report by {self.reported_by.email} "  # type: ignore
            f"against {self.reported_user.email} "  # type: ignore
            f"for {self.get_reason_display().lower()} "
            f"on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')} "
            f"- Status: {self.get_status_display()}"
        )
