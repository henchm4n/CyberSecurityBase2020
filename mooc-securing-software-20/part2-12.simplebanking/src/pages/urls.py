from django.urls import path

from .views import homePageView, addView

urlpatterns = [
    path('', homePageView, name='home'),
    path('add/', addView, name='add'),
]
