from django.urls import path

from . import views


app_name = 'pages'

urlpatterns: list = [
    path('about/', views.AboutView.as_view(), name='about'),
    path('rules/', views.RulesView.as_view(), name='rules'),
]
