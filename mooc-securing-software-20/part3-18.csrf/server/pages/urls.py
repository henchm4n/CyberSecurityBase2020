from django.urls import path

from .views import homePageView, transferView, confirmView

urlpatterns = [
    path('', homePageView, name='home'),
    path('transfer/', transferView, name='transfer'),
    path('confirm/', confirmView, name='confirm')
]
