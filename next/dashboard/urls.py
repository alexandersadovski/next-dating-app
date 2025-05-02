from django.urls import path, include
from next.dashboard import views

urlpatterns = [
    path('', views.show_user, name='show-user'),
    path('matches/', include('next.matches.urls')),
    path('', include('next.messaging.urls')),
    path('reports/', include('next.reports.urls')),
]
