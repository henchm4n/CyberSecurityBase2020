from django.urls import path

from .views import homePageView, taskView, addView

urlpatterns = [
    path('', homePageView, name='home'),
    path('tasks', taskView, name='tasks'),
    path('add', addView, name='add'),
]
