
from django.contrib import admin
from django.urls import path,include


from django.conf import settings
from django.conf.urls.static import static



admin.site.site_header = "BLoogy Admin"
admin.site.site_title = "BLoogyAdmin DashBoard"
admin.site.index_title = "Welcome to BLoogyAdmin DashBoard"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),


]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)