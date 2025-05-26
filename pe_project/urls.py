from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path(
        "accounts/", include("accounts.urls", namespace="accounts")
    ),  # Custom accounts URLs
    path("", include("pages.urls")),
    path("lessons/", include("lessons.urls", namespace="lessons")),
    re_path(
        r"^lessons/lessons/$", RedirectView.as_view(url="/lessons/", permanent=True)
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
