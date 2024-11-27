from django.conf import settings
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
