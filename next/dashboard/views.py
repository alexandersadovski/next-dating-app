from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from next.accounts.models import Profile
from next.dashboard.models import UserInteraction
from next.matches.models import Match


@login_required
def show_user(request):
    user = request.user
    user_profile = Profile.objects.get(user=user)

    seen_profiles = UserInteraction.objects.filter(user=user).values_list('target_user_id', flat=True)
    next_profile = (
        Profile.objects
        .exclude(user=user)
        .exclude(user__id__in=seen_profiles)
        .exclude(user__is_superuser=True)
        .exclude(user__is_staff=True)
        .exclude(gender=user_profile.gender)
        .order_by('?')
        .first())

    if request.method == 'POST':
        liked = 'like' in request.POST
        UserInteraction.objects.create(
            user=user,
            target_user=next_profile.user,
            liked=liked,
        )

        if liked:
            if UserInteraction.check_match(request.user, next_profile.user):
                Match.create_match(user1=request.user, user2=next_profile.user)

                context = {
                    'profile': next_profile,
                    'match_data': {'name': f'{next_profile.first_name} {next_profile.last_name}'}
                }
                return render(request, 'dashboard/dashboard.html', context=context)

        return redirect('show-user')

    return render(request, 'dashboard/dashboard.html', context={'profile': next_profile})
