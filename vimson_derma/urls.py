from django.contrib import admin
from django.urls import path, include
import debug_toolbar

urlpatterns = [
    path("jet/", include("jet.urls", "jet")),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("__debug__/", include(debug_toolbar.urls)),
]
