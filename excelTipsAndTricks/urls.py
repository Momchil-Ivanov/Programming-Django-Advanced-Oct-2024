from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('excelTipsAndTricks.common.urls')),
    path('accounts/', include('excelTipsAndTricks.accounts.urls')),
    path('categories/', include('excelTipsAndTricks.categories.urls')),
    path('tips/', include('excelTipsAndTricks.tips.urls')),
    path('tags/', include('excelTipsAndTricks.tags.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)