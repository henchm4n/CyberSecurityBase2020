from django.urls import path

from .views import addPageView
from .views import multiplyPageView

urlpatterns = [
    path('add/', addPageView, name='add'),
    path('multiply/', multiplyPageView, name='multiply')
]
