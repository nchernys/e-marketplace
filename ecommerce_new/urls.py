
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('new_shop.urls')),
    path('users/', include('users.urls')),
    path('', include('django.contrib.auth.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT); 
static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
