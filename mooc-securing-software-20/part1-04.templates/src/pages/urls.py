from django.urls import path

from .views import homePageView, videoPageView

urlpatterns = [
    path('', homePageView, name='home'),
    path('video/', videoPageView, name='video')
]
