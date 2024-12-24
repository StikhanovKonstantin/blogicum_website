from django.contrib import admin
from django.urls import include, path
from django.views.generic.edit import CreateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        CreateView.as_view()
    )
]

# Переопределеяем страницу ошибки 404.
handler404 = 'core.views.page_not_found'

# Переопределяем страницу ошибки 500.
handler500 = 'core.views.server_failure'
