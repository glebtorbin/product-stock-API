from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as doc
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls'))
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns+=doc