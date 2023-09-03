from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) # agregamos la ruta de los archivos media 

urlpatterns +=[re_path(r'^.*',
                        TemplateView.as_view(template_name='index.html'))] # Estamos accediendo a nuestra pagina de react   

