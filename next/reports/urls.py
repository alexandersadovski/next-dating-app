from django.urls import path
from next.reports import views

urlpatterns = [
    path('', views.show_reports, name='show-reports')
]
