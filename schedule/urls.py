from django.urls import path
from . import views

urlpatterns = [
    # '' contains string after /blog
    path('', views.home, name='schedule-home'),
]
