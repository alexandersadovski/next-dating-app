from django.shortcuts import redirect
from django.urls import reverse


class RestrictSpecialUsersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
            if not request.path.startswith('/admin/'):
                return redirect(reverse('admin:index'))

        response = self.get_response(request)
        return response
