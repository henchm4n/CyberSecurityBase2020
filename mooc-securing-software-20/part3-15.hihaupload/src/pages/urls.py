from django.urls import path

from .views import homePageView, addView, deleteView, downloadView

urlpatterns = [
    path('', homePageView, name='home'),
    path('add/', addView, name='add'),
    path('download/<int:fileid>', downloadView, name='add'),
    path('delete/', deleteView, name='delete'),
]
