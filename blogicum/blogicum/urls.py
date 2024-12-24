from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('blog:index')
        ),
        name='registration'
    ),
]

# Переопределеяем страницу ошибки 404.
handler404 = 'core.views.page_not_found'

# Переопределяем страницу ошибки 500.
handler500 = 'core.views.server_failure'
