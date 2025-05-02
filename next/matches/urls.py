from django.urls import path
from next.matches import views

urlpatterns = [
    path('', views.list_matches, name='matches'),
]
