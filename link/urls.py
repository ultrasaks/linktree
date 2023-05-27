from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', include('customing_app.urls')),
    path('', include('welcome_app.urls')),
    path('l/', include('show_app.urls')),
]

urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#! WELCOME -- login, register, logout, landing
#! CUSTOMISING -- info, links, color theme, delete
#! SHOW -- /l/ -- links