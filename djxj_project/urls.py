from django.conf import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("ornamental-actuary/", admin.site.urls),
    path("users/", include("django.contrib.auth.urls")),
    path("accounts/", include("allauth.urls")),
    path("", include("pages.urls")),
]

# In debug, add url to django-debug-toolbar
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls)),] + urlpatterns
