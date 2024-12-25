from django.views.generic import TemplateView


class AboutView(TemplateView):
    """Страница с информацией 'О компании'."""

    template_name = 'pages/about.html'


class RulesView(TemplateView):
    """Страница с информацией правил компании."""

    template_name = 'pages/rules.html'
