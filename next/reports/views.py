from django.shortcuts import render
from next.reports.models import Report


def show_reports(request):
    reports = Report.objects.filter(reported_by=request.user)
    return render(request, 'dashboard/reports.html', context={'reports': reports})
