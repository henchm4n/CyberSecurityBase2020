from django.urls import path

from .views import homePageView, addPageView, erasePageView

urlpatterns = [
    path('', homePageView, name='home'),
    path('add', addPageView, name='add'),
    path('erase', erasePageView, name='erase')
]
