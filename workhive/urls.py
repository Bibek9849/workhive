
from django.contrib import admin
from django.urls import path,include
from django.conf import settings

# from admin_register.views import 

admin.site.site_header = "     WorkHive    "
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("backend_crud.urls")),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT)                          