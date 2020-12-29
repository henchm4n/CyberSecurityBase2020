from django.urls import path

from .views import homePageView, addView, mailView

urlpatterns = [
    path('', homePageView, name='home'),
    path('add/', addView, name='add'),
    path('mail/', mailView, name='mail'),
]
