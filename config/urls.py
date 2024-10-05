from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from config import settings
from etudiant.views import index_view 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
