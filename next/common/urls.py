from django.urls import path
from next.common import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('coming-soon/', views.ComingSoonView.as_view(), name='coming-soon'),
]
