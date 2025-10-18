from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [ 
    path('admin/', admin.site.urls),
    #Include ayuda a django a reconocer las rutas de las aplicaciones
    #Pasandole como argumento la ruta de las urls
    path('', include('portfolio.urls')),
    path('blog/', include('blog.urls')),
    
    #Se agrega esta linea para que django reconozca los archivos estaticos
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
