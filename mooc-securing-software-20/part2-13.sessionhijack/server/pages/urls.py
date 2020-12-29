from django.urls import path

from .views import homePageView, balanceView

urlpatterns = [
    path('', homePageView, name='home'),
    path('balance/', balanceView, name='balance'),
]
