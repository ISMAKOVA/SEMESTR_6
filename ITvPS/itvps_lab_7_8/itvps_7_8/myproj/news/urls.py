from django.urls import path
from . import views

urlpatterns = [
    path('', views.article),
    path('index', views.index),
    path('rubrika', views.rubrika)
]
