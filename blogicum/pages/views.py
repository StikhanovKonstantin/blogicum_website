from django.views.generic import TemplateView
from django.shortcuts import render

# Импорт констант со статусами из Класса(Enum).
from .statuses import Statuses


class AboutView(TemplateView):
    """Страница с информацией 'О компании'."""

    template_name = 'pages/about.html'


class RulesView(TemplateView):
    """Страница с информацией правил компании."""

    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    return render(
        request, 'pages/404.html', status=Statuses.ERROR_404.value
    )


def csrf_failure(request, reason=''):
    return render(
        request, 'pages/403csrf.html', status=Statuses.ERROR_403.value
    )


def server_failure(request):
    return render(
        request, 'pages/500.html', status=Statuses.ERROR_500.value
    )
