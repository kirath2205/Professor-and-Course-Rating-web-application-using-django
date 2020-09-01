from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
admin.site.site_header='Professor and Course Rating'
admin.site.site_title='Professor and Course Rating Admin'
admin.site.index_title='Welcome to Professor and Course Rating Admin'
urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('',include('mainsite.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
