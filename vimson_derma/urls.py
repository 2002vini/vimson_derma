from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from . views import upload_image

from django.conf.urls.static import static

import debug_toolbar

urlpatterns = [
    path("jet/", include("jet.urls", "jet")),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    path("admin/", admin.site.urls),
    path("", include("api.urls")),
    path("__debug__/", include(debug_toolbar.urls)),
    path("tinymce/", include("tinymce.urls")),
    path("upload_image/", upload_image, name="upload_image"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
