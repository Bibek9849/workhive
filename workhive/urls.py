from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

admin.site.site_header = "     WorkHive    "

# Base URL patterns that should NOT be translated (language-switcher)
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

# Translatable URLs go inside i18n_patterns
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('backend_crud.urls')),
    prefix_default_language=True
)

# Add media and static files **OUTSIDE** i18n_patterns
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
