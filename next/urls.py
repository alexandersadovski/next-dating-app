from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from next import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('next.accounts.urls')),
    path('dashboard/', include('next.dashboard.urls')),
    path('', include('next.common.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
