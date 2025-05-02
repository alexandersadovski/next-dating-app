from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from next.matches.models import Match
from next.accounts.models import AppUser
from next.reports.forms import ReportForm


@login_required
def list_matches(request):
    matches = Match.objects.filter(user1=request.user) | Match.objects.filter(user2=request.user)

    if request.method == 'POST':
        form = ReportForm(request.POST)
        reported_user_id = request.POST.get('user_id')
        reported_user = get_object_or_404(AppUser, pk=reported_user_id)

        if form.is_valid():
            report = form.save(commit=False)
            report.reported_by = request.user
            report.reported_user = reported_user
            report.save()

            return redirect('matches')
    else:
        form = ReportForm()

    return render(request, 'dashboard/matches.html', {'matches': matches, 'form': form})
