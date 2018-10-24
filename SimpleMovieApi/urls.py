from django.contrib import admin
from django.conf.urls import include, url


urlpatterns = [
    url(r'^', include('movie.urls')),
    url(r'^', include('comment.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls'))
]
